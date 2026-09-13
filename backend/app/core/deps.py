from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.identity import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    """Resolve the currently authenticated admin from the bearer token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    admin_id = payload.get("sub")
    if admin_id is None:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id == int(admin_id), Admin.is_active.is_(True)).first()
    if admin is None:
        raise credentials_exception
    return admin


def require_permission(permission_code: str):
    """
    Dependency factory for role-based authorization.
    Usage: Depends(require_permission("services.manage"))
    """

    def _checker(admin: Admin = Depends(get_current_admin)) -> Admin:
        if admin.role is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No role assigned")
        codes = {perm.code for perm in admin.role.permissions}
        if permission_code not in codes and "*" not in codes:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return admin

    return _checker
