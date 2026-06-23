import uuid
from datetime import datetime

from pydantic import BaseModel


class PropertyTypeInfo(BaseModel):
    code: str
    display_name: str


class CreatePropertyTypeRequest(PropertyTypeInfo):
    pass


class UpdatePropertyTypeRequest(PropertyTypeInfo):
    pass


class PropertyTypeResponse(PropertyTypeInfo):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


PropertyTypeListResponse = list[PropertyTypeResponse]
