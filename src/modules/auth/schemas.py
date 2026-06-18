import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.data.entities.user import UserRole


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    username: str
    phone: str | None = None
    email: str | None = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
