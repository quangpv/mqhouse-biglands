import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.shared.pagination import PaginatedResponse


class QueueCountResponse(BaseModel):
    approval_type: str
    transaction_type: str
    count: int


class QueueListResponse(BaseModel):
    queues: list[QueueCountResponse]


class QueueItemResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    listing_code: str
    approval_type: str
    transaction_type: str
    title: str | None = None
    price: Decimal | None = None
    status: str
    created_at: datetime
    customer_name: str | None = None
    customer_phone: str | None = None
    deposit_amount: Decimal | None = None
    event_notes: str | None = None


class QueueItemListResponse(PaginatedResponse):
    data: list[QueueItemResponse]


class ApprovalDetailResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    listing_code: str
    approval_type: str
    transaction_type: str
    title: str | None = None
    price: Decimal | None = None
    listing_status: str
    created_at: datetime
    customer_name: str | None = None
    customer_phone: str | None = None
    deposit_amount: Decimal | None = None
    event_notes: str | None = None
    has_existing_approval: bool = False
    existing_decision: str | None = None


class RejectRequest(BaseModel):
    reason: str = Field(..., min_length=1, max_length=1000)


class BulkApproveRequest(BaseModel):
    listing_ids: list[uuid.UUID] = Field(..., min_length=1, max_length=50)


class BulkApproveItem(BaseModel):
    listing_id: uuid.UUID
    success: bool
    message: str


class BulkApproveResponse(BaseModel):
    results: list[BulkApproveItem]
    total: int
    succeeded: int
    failed: int


class ApproveResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    listing_code: str
    approval_type: str
    decision: str
    listing_status: str
    created_at: datetime
