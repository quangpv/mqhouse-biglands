import uuid
from datetime import datetime

from pydantic import BaseModel

from src.shared.pagination import PaginatedResponse


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    body: str
    reference_type: str | None = None
    reference_id: uuid.UUID | None = None
    is_read: bool
    event_type: str | None = None
    actor_name: str | None = None
    transaction_type: str | None = None
    created_at: datetime


class NotificationListResponse(PaginatedResponse):
    data: list[NotificationResponse]
    unread_count: int = 0
    category_counts: dict[str, int] = {}


class UnreadCountResponse(BaseModel):
    count: int
