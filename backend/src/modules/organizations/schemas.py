import uuid
from datetime import datetime

from pydantic import BaseModel


class OrganizationInfo(BaseModel):
    name: str
    display_name: str
    transaction_types: list[uuid.UUID]
    property_types: list[uuid.UUID]


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    transaction_types: list[uuid.UUID]
    property_types: list[uuid.UUID]
    created_at: datetime


class CreateOrganizationRequest(OrganizationInfo):
    pass


class UpdateOrganizationRequest(OrganizationInfo):
    pass


OrganizationListResponse = list[OrganizationResponse]
