import uuid
from datetime import datetime

from pydantic import BaseModel

from src.modules.properties.schemas import PropertyResponse


class PromoteToHotRequest(BaseModel):
    start_time: datetime
    end_time: datetime


class HotPropertyResponse(BaseModel):
    id: uuid.UUID
    property: PropertyResponse
    start_time: datetime
    end_time: datetime
    created_by: uuid.UUID
    created_at: datetime


HotPropertyListResponse = list[HotPropertyResponse]
