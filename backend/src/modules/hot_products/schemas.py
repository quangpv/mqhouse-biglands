import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PromoteToHotRequest(BaseModel):
    listing_id: uuid.UUID


class HotListingResponse(BaseModel):
    id: uuid.UUID
    code: str
    transaction_type: str
    property_type: str
    title: str | None = None
    price: Decimal
    status: str
    hot_order: int | None = None
    view_count: int | None = 0
    created_by_id: uuid.UUID
    created_at: datetime


class ReorderHotListingsRequest(BaseModel):
    listing_ids: list[uuid.UUID] = Field(..., min_length=1, max_length=14)
