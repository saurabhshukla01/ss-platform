from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.operations import AuditLog
from app.schemas.audit import AuditLogOut

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("", response_model=list[AuditLogOut], dependencies=[Depends(require_permission("audit.view"))])
def list_audit_logs(module: str | None = None, admin_id: int | None = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(AuditLog)
    if module:
        query = query.filter(AuditLog.module == module)
    if admin_id:
        query = query.filter(AuditLog.admin_id == admin_id)
    return query.order_by(AuditLog.created_at.desc()).limit(min(limit, 500)).all()
