from fastapi import Request
from sqlalchemy.orm import Session

from app.models.operations import AuditLog


def log_action(
    db: Session,
    admin_id: int | None,
    action: str,
    module: str,
    record_id: str | int | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
    request: Request | None = None,
) -> None:
    """Write an audit trail entry. Call this alongside db.commit() in admin write endpoints."""
    db.add(AuditLog(
        admin_id=admin_id,
        action=action,
        module=module,
        record_id=str(record_id) if record_id is not None else None,
        old_value=old_value,
        new_value=new_value,
        ip_address=request.client.host if request and request.client else None,
    ))
