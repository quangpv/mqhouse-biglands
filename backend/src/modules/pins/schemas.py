import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.shared.pagination import PaginatedResponse


class PinnedListingResponse(BaseModel):
    id: uuid.UUID
    code: str
    transaction_type: str
    property_type: str
    title: str | None = None
    description: str
    price: Decimal
    status: str
    is_hot: bool | None = False
    view_count: int | None = 0
    created_by_id: uuid.UUID
    created_at: datetime
    is_pinned: bool = True


class PinnedListingListResponse(PaginatedResponse):
    data: list[PinnedListingResponse]
