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
    email: str
    is_super_admin: bool
    role_name: str | None = None

    class Config:
        from_attributes = True