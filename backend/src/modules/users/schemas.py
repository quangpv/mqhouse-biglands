import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.data.entities.user import UserRole


class CreateUserRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    username: str = Field(..., min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)
    password: str = Field(..., min_length=6)
    role: UserRole
    organization_id: uuid.UUID | None = None
    property_type_ids: list[uuid.UUID] = []
    transaction_type_ids: list[uuid.UUID] = []


class UpdateUserRequest(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)
    is_active: bool | None = None
    organization_id: uuid.UUID | None = None
    role: UserRole | None = None
    property_type_ids: list[uuid.UUID] | None = None
    transaction_type_ids: list[uuid.UUID] | None = None


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
    property_type_ids: list[uuid.UUID]
    transaction_type_ids: list[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class PageDTO(BaseModel):
    page: int
    size: int
    total_pages: int


class UserListData(BaseModel):
    data: list[UserResponse]
    metadata: PageDTO
