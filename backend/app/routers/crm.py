from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.models.crm import Lead, LeadNote, LeadFollowup, LeadStatusHistory
from app.models.identity import Admin
from app.schemas.crm import LeadOut, LeadStatusUpdate, LeadNoteCreate, LeadFollowupCreate

router = APIRouter(prefix="/crm/leads", tags=["CRM"])


@router.get("", response_model=list[LeadOut], dependencies=[Depends(require_permission("crm.view"))])
def list_leads(status_filter: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Lead)
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    return query.order_by(Lead.created_at.desc()).all()


@router.get("/{lead_id}", response_model=LeadOut, dependencies=[Depends(require_permission("crm.view"))])
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lead not found")
    return lead


@router.patch("/{lead_id}/status", response_model=LeadOut, dependencies=[Depends(require_permission("crm.manage"))])
def update_lead_status(lead_id: int, payload: LeadStatusUpdate, db: Session = Depends(get_db),
                        admin: Admin = Depends(get_current_admin)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lead not found")

    old_status = lead.status
    lead.status = payload.status
    db.add(LeadStatusHistory(lead_id=lead.id, admin_id=admin.id, from_status=old_status, to_status=payload.status))
    if payload.note:
        db.add(LeadNote(lead_id=lead.id, admin_id=admin.id, note=payload.note))

    db.commit()
    db.refresh(lead)
    return lead


@router.post("/{lead_id}/notes", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("crm.manage"))])
def add_lead_note(lead_id: int, payload: LeadNoteCreate, db: Session = Depends(get_db),
                   admin: Admin = Depends(get_current_admin)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lead not found")
    note = LeadNote(lead_id=lead_id, admin_id=admin.id, note=payload.note)
    db.add(note)
    db.commit()
    return {"ok": True, "note_id": note.id}


@router.post("/{lead_id}/followups", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("crm.manage"))])
def add_lead_followup(lead_id: int, payload: LeadFollowupCreate, db: Session = Depends(get_db),
                       admin: Admin = Depends(get_current_admin)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lead not found")
    followup = LeadFollowup(
        lead_id=lead_id, admin_id=admin.id,
        scheduled_at=payload.scheduled_at, channel=payload.channel,
    )
    db.add(followup)
    db.commit()
    return {"ok": True, "followup_id": followup.id}
