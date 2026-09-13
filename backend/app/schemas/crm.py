from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.crm import LeadStatus


class InquiryCreate(BaseModel):
    """Public 'Get Quote' / Contact Us form submission."""

    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = None
    service_id: int | None = None
    budget_range: str | None = None
    timeline: str | None = None
    preferred_contact_method: str | None = None  # email | phone | whatsapp
    message: str | None = None
    source: str | None = None


class InquiryOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    service_id: int | None
    budget_range: str | None
    timeline: str | None
    preferred_contact_method: str | None
    message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadOut(BaseModel):
    id: int
    inquiry_id: int | None
    customer_id: int | None
    assigned_admin_id: int | None
    status: LeadStatus
    source: str | None
    estimated_value: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadStatusUpdate(BaseModel):
    status: LeadStatus
    note: str | None = None


class LeadNoteCreate(BaseModel):
    note: str = Field(min_length=1)


class LeadFollowupCreate(BaseModel):
    scheduled_at: datetime
    channel: str | None = None
