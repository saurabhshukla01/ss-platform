from datetime import datetime
from pydantic import BaseModel, Field


class CommunicationLogOut(BaseModel):
    id: int
    lead_id: int | None
    customer_id: int | None
    channel: str
    direction: str
    subject: str | None
    status: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class CommunicationLogCreate(BaseModel):
    lead_id: int | None = None
    customer_id: int | None = None
    channel: str = Field(description="email | whatsapp | call | sms")
    direction: str = "outbound"
    subject: str | None = None
    body: str | None = None
    status: str | None = "sent"


class NotificationOut(BaseModel):
    id: int
    title: str
    body: str | None
    link_url: str | None
    is_read: bool
    created_at: datetime
    model_config = {"from_attributes": True}
