import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.data.entities.user import UserRole
from src.shared.pagination import PaginatedResponse


class CreateUserRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    username: str = Field(..., min_length=3, max_length=100)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.AGENT


class UpdateUserRequest(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)


class AssignRoleRequest(BaseModel):
    role: UserRole


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

    model_config = {"from_attributes": True}


class UserListResponse(PaginatedResponse):
    data: list[UserResponse]
