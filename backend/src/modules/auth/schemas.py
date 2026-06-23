import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.data.entities.user import UserRole


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)


class ChangePasswordResponse(BaseModel):
    message: str


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)


class ForgotPasswordResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)


class ResetPasswordResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    username: str
    phone: str | None = None
    email: str | None = None
    role: UserRole
    is_active: bool
    organization_id: str | None = None
    organization_name: str | None = None
    created_at: datetime
    updated_at: datetime
