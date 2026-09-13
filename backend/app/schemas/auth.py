from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminMe(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_super_admin: bool
    role_name: str | None = None

    model_config = {"from_attributes": True}
