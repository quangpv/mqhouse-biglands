import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.data.entities.listing import CommissionType, ListingStatus, PropertyType, TransactionType
from src.shared.pagination import PaginatedResponse


class CreateListingRequest(BaseModel):
    transaction_type: TransactionType = TransactionType.BAN
    property_type: PropertyType
    title: str | None = Field(None, max_length=500)
    description: str
    price: Decimal = Field(..., gt=0)
    commission_type: CommissionType
    commission_value: Decimal = Field(..., ge=0)
    area_width: Decimal = Field(..., gt=0)
    area_length: Decimal = Field(..., gt=0)
    total_area: Decimal = Field(..., gt=0)
    num_rooms: int = 0
    num_bathrooms: int = 0
    num_floors: int = 0
    street_name: str
    house_number: str
    address: str
    ward: str
    district: str
    city: str = "Hồ Chí Minh"
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    label: str | None = Field(None, max_length=100)
    furnishing: str | None = None
    frontage_type: str | None = None
    legal_status: str | None = None
    direction: str | None = None
    road_width: str | None = None
    owner_phone: str
    video_url: str | None = None
    action: str | None = None  # "submit" to immediately submit for approval


class UpdateListingRequest(BaseModel):
    transaction_type: TransactionType | None = None
    property_type: PropertyType | None = None
    title: str | None = Field(None, max_length=500)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    commission_type: CommissionType | None = None
    commission_value: Decimal | None = Field(None, ge=0)
    area_width: Decimal | None = Field(None, gt=0)
    area_length: Decimal | None = Field(None, gt=0)
    total_area: Decimal | None = Field(None, gt=0)
    num_rooms: int | None = None
    num_bathrooms: int | None = None
    num_floors: int | None = None
    street_name: str | None = None
    house_number: str | None = None
    address: str | None = None
    ward: str | None = None
    district: str | None = None
    city: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    label: str | None = None
    furnishing: str | None = None
    frontage_type: str | None = None
    legal_status: str | None = None
    direction: str | None = None
    road_width: str | None = None
    owner_phone: str | None = None
    video_url: str | None = None
    action: str | None = None  # "submit" to immediately submit for approval after update


class ListingResponse(BaseModel):
    id: uuid.UUID
    code: str
    transaction_type: TransactionType
    property_type: PropertyType
    title: str | None = None
    description: str
    price: Decimal
    commission_type: CommissionType
    commission_value: Decimal
    area_width: Decimal
    area_length: Decimal
    total_area: Decimal
    num_rooms: int
    num_bathrooms: int
    num_floors: int
    street_name: str
    house_number: str
    address: str
    ward: str
    district: str
    city: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    label: str | None = None
    furnishing: str | None = None
    frontage_type: str | None = None
    legal_status: str | None = None
    direction: str | None = None
    road_width: str | None = None
    owner_phone: str
    video_url: str | None = None
    status: ListingStatus
    is_hot: bool | None = False
    hot_order: int | None = None
    view_count: int | None = 0
    created_by_id: uuid.UUID
    approved_by_id: uuid.UUID | None = None
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ListingDetailResponse(ListingResponse):
    images: list = []
    deal_events: list = []
    is_pinned: bool = False


class ListingListResponse(PaginatedResponse):
    data: list[ListingResponse]
    total_count: int = 0
