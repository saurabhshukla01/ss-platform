from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_admin
from app.models.identity import Admin
from app.schemas.auth import TokenResponse, AdminMe

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Admin Panel login. Uses OAuth2 password form (username = email) so it
    works directly with FastAPI's built-in Swagger 'Authorize' button.
    """
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not admin.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is disabled")

    token = create_access_token(subject=str(admin.id), extra_claims={"is_super_admin": admin.is_super_admin})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=AdminMe)
def get_me(admin: Admin = Depends(get_current_admin)):
    return AdminMe(
        id=admin.id,
        full_name=admin.full_name,
        email=admin.email,
        is_super_admin=admin.is_super_admin,
        role_name=admin.role.name if admin.role else None,
    )
