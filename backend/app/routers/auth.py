from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.core.deps import get_current_admin
from app.models.identity import Admin
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    AdminMe,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Admin login using email and password.
    """

    admin = (
        db.query(Admin)
        .filter(
            Admin.email == login_data.email
        )
        .first()
    )

    # -----------------------------------------------------
    # User not found
    # -----------------------------------------------------

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # -----------------------------------------------------
    # Password verification
    # -----------------------------------------------------

    if not verify_password(
        login_data.password,
        admin.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # -----------------------------------------------------
    # Account status
    # -----------------------------------------------------

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # -----------------------------------------------------
    # JWT
    # -----------------------------------------------------

    token = create_access_token(
        subject=str(admin.id),
        extra_claims={
            "is_super_admin": admin.is_super_admin,
        },
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


# =========================================================
# CURRENT ADMIN
# =========================================================

@router.get(
    "/me",
    response_model=AdminMe,
)
def get_me(
    admin: Admin = Depends(get_current_admin),
):
    """
    Return currently authenticated admin.
    """

    return AdminMe(
        id=admin.id,
        full_name=admin.full_name,
        email=admin.email,
        is_super_admin=admin.is_super_admin,
        role_name=(
            admin.role.name
            if admin.role
            else None
        ),
    )