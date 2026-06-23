from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.modules.properties.schemas import PageDTO


class NotificationListParams(BaseModel):
    is_read: bool | None = None
    page: int = 1
    size: int = 20


class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    body: str | None
    reference_type: str | None
    reference_id: UUID | None
    is_read: bool
    event_type: str | None
    actor_name: str | None
    transaction_type: str | None
    created_at: datetime


class NotificationListResponse(BaseModel):
    data: list[NotificationResponse]
    metadata: PageDTO


class NotificationCountResponse(BaseModel):
    count: int


class ReadAllResponse(BaseModel):
    message: str
