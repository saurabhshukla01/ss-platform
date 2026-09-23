from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin
from app.models.operations import CommunicationLog, Notification
from app.schemas.communication import CommunicationLogOut, CommunicationLogCreate, NotificationOut

router = APIRouter(prefix="/communication", tags=["Communication"])


@router.get("/logs", response_model=list[CommunicationLogOut], dependencies=[Depends(require_permission("crm.view"))])
def list_logs(lead_id: int | None = None, customer_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(CommunicationLog)
    if lead_id:
        query = query.filter(CommunicationLog.lead_id == lead_id)
    if customer_id:
        query = query.filter(CommunicationLog.customer_id == customer_id)
    return query.order_by(CommunicationLog.created_at.desc()).all()


@router.post("/logs", response_model=CommunicationLogOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("crm.manage"))])
def create_log(payload: CommunicationLogCreate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    row = CommunicationLog(**payload.model_dump(), admin_id=admin.id)
    db.add(row)
    db.flush()
    log_action(db, admin.id, "create", "communication_logs", row.id, new_value={"channel": payload.channel}, request=request)
    db.commit()
    db.refresh(row)
    return row


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return (
        db.query(Notification)
        .filter(Notification.admin_id == admin.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )


@router.patch("/notifications/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(notification_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.admin_id == admin.id).first()
    if not notif:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Notification not found")
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif
