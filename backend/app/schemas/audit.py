from datetime import datetime
from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: int
    admin_id: int | None
    action: str
    module: str
    record_id: str | None
    old_value: dict | None
    new_value: dict | None
    ip_address: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
