from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.identity import Admin


security = HTTPBearer()


# ---------------------------------------------------------
# GET CURRENT ADMIN
# ---------------------------------------------------------

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Admin:

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        admin_id = payload.get("sub")

        if admin_id is None:
            raise credentials_exception

        admin_id = int(admin_id)

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    admin = (
        db.query(Admin)
        .filter(Admin.id == admin_id)
        .first()
    )

    if admin is None:
        raise credentials_exception

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    return admin


# ---------------------------------------------------------
# SUPER ADMIN CHECK
# ---------------------------------------------------------

def require_super_admin(
    admin: Admin = Depends(get_current_admin),
) -> Admin:

    if not admin.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required",
        )

    return admin


# ---------------------------------------------------------
# PERMISSION CHECK
# ---------------------------------------------------------

def require_permission(permission_name: str) -> Callable:

    def permission_dependency(
        admin: Admin = Depends(get_current_admin),
    ) -> Admin:

        # Super admin has access to everything
        if admin.is_super_admin:
            return admin

        # Get admin role
        role = getattr(admin, "role", None)

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin role is not assigned",
            )

        # Get role permissions
        permissions = getattr(role, "permissions", []) or []

        # Check permission
        has_permission = any(
            getattr(permission, "name", None) == permission_name
            for permission in permissions
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission_name}",
            )

        return admin

    return permission_dependency