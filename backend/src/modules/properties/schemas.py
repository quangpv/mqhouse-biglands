import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from src.data.entities.property import CommissionType, DirectionType, PropertyStatus


class FileInfo(BaseModel):
    id: uuid.UUID
    origin_name: str
    path: str
    mimetype: str
    created_by: uuid.UUID
    entity_type: str
    size: int


class CreatorInfo(BaseModel):
    id: uuid.UUID
    full_name: str
    phone: str | None = None


class PageDTO(BaseModel):
    page: int
    size: int
    total_pages: int


class NumberRange(BaseModel):
    from_field: int | Decimal | None = Field(None, alias="from")
    to: int | Decimal | None = None


class PropertyInfo(BaseModel):
    transaction_type_id: uuid.UUID
    property_type_id: uuid.UUID
    title: str | None = None
    description: str
    price: Decimal
    commission_type: CommissionType
    commission_value: Decimal
    area_width: Decimal
    area_length: Decimal
    total_area: Decimal
    num_rooms: int = 0
    num_bathrooms: int = 0
    num_floors: int = 0
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
    direction: DirectionType | None = None
    road_width: str | None = None
    owner_phone: str | None = None
    video_url: str | None = None
    image_ids: list[uuid.UUID] = []


class CreatePropertyRequest(PropertyInfo):
    type: Literal["draft", "post_pending"] = "draft"


class UpdatePropertyRequest(BaseModel):
    transaction_type_id: uuid.UUID | None = None
    property_type_id: uuid.UUID | None = None
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    commission_type: CommissionType | None = None
    commission_value: Decimal | None = None
    area_width: Decimal | None = None
    area_length: Decimal | None = None
    total_area: Decimal | None = None
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
    direction: DirectionType | None = None
    road_width: str | None = None
    owner_phone: str | None = None
    video_url: str | None = None
    image_ids: list[uuid.UUID] | None = None


class PropertyResponse(BaseModel):
    id: uuid.UUID
    code: str
    transaction_type_id: uuid.UUID
    transaction_type_code: str | None = None
    property_type_id: uuid.UUID
    property_type_code: str | None = None
    title: str | None = None
    description: str
    price: Decimal
    commission_type: CommissionType
    commission_value: Decimal
    area_width: Decimal
    area_length: Decimal
    total_area: Decimal
    price_per_m2: Decimal | None = None
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
    direction: DirectionType | None = None
    road_width: str | None = None
    owner_phone: str | None = None
    video_url: str | None = None
    status: PropertyStatus
    is_hot: bool | None = None
    hot_order: int | None = None
    view_count: int
    primary_image_url: str | None = None
    images: list[FileInfo] = []
    created_by_id: uuid.UUID
    creator: CreatorInfo | None = None
    is_pinned: bool = False
    requires_approval: bool = False
    created_at: datetime
    updated_at: datetime


class PropertyListResponse(BaseModel):
    data: list[PropertyResponse]
    metadata: PageDTO


class DepositRequest(BaseModel):
    notes: str | None = None
    customer_name: str
    customer_phone: str
    contract_date: date
    file_ids: list[uuid.UUID] = []


class CompleteRequest(BaseModel):
    notes: str | None = None
    customer_name: str
    customer_phone: str
    contract_date: date
    file_ids: list[uuid.UUID] = []


class NotesRequest(BaseModel):
    notes: str | None = None


class PropertyTransitionResponse(BaseModel):
    id: uuid.UUID
    property_id: uuid.UUID
    from_status: PropertyStatus | None = None
    to_status: PropertyStatus
    action: str
    actor_id: uuid.UUID
    actor_name: str
    notes: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    contract_date: date | None = None
    file_ids: list[uuid.UUID] = []
    created_at: datetime


PropertyTransitionListResponse = list[PropertyTransitionResponse]
