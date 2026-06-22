import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.shared.pagination import PaginatedResponse



class DealEventInfo(BaseModel):
    event_type: str
    notes: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    deposit_amount: Decimal | None = None
    created_at: datetime


class ReporterInfo(BaseModel):
    id: uuid.UUID
    full_name: str | None = None
    email: str


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
    deal_event: DealEventInfo | None = None
    reported_by: ReporterInfo | None = None
    total_area: Decimal | None = None
    price_per_m2: Decimal | None = None
    area_width: Decimal | None = None
    area_length: Decimal | None = None
    num_rooms: int = 0
    num_bathrooms: int = 0
    num_floors: int = 0
    street_name: str = ""
    ward: str = ""
    district: str = ""
    city: str = ""
    address: str = ""
    is_hot: bool = False
    is_pinned: bool = False
    hot_order: int | None = None
    primary_image_url: str | None = None
    created_by_id: uuid.UUID | None = None
    creator_name: str | None = None
    listing_created_at: datetime | None = None


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
