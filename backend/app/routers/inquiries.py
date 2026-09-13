from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.crm import Inquiry, Lead, LeadStatus, LeadStatusHistory
from app.schemas.crm import InquiryCreate, InquiryOut

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("", response_model=InquiryOut, status_code=status.HTTP_201_CREATED)
def submit_inquiry(payload: InquiryCreate, db: Session = Depends(get_db)):
    """
    Public endpoint used by the Contact Us and Get Quote pages.
    Automatically creates a NEW lead in the CRM pipeline for follow-up.
    """
    inquiry = Inquiry(**payload.model_dump())
    db.add(inquiry)
    db.flush()  # get inquiry.id before commit

    lead = Lead(inquiry_id=inquiry.id, status=LeadStatus.NEW, source=payload.source)
    db.add(lead)
    db.flush()

    db.add(LeadStatusHistory(lead_id=lead.id, from_status=None, to_status=LeadStatus.NEW))

    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.get("/admin", response_model=list[InquiryOut], dependencies=[Depends(require_permission("crm.view"))])
def list_inquiries(db: Session = Depends(get_db)):
    return db.query(Inquiry).order_by(Inquiry.created_at.desc()).all()


@router.get("/admin/{inquiry_id}", response_model=InquiryOut, dependencies=[Depends(require_permission("crm.view"))])
def get_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Inquiry not found")
    return inquiry
