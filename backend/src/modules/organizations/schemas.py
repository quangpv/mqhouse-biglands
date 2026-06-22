import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.shared.pagination import PaginatedResponse


class CreateOrganizationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)


class UpdateOrganizationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrganizationListResponse(PaginatedResponse):
    data: list[OrganizationResponse]
