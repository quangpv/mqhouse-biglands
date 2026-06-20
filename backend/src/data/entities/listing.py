import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

_values_callable = lambda x: [e.value for e in x]  # noqa: E731


class TransactionType(PyEnum):
    SANG_NHUONG = "SANG_NHUONG"
    CHO_THUE = "CHO_THUE"
    BAN = "BAN"


class PropertyType(PyEnum):
    NHA_PHO = "NHA_PHO"
    CAN_HO = "CAN_HO"
    CHDV = "CHDV"
    DAT = "DAT"
    BIET_THU = "BIET_THU"
    VAN_PHONG = "VAN_PHONG"
    MAT_BANG = "MAT_BANG"
    KHO_XUONG = "KHO_XUONG"
    NHA_TRO = "NHA_TRO"
    KHAC = "KHAC"


class CommissionType(PyEnum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"


class ListingStatus(PyEnum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    CON_HANG = "CON_HANG"
    DA_COC = "DA_COC"
    DA_CHOT = "DA_CHOT"
    HUY_COC = "HUY_COC"
    HET_HANG = "HET_HANG"
    QUA_HAN = "QUA_HAN"


class ListingEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "listings"

    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, values_callable=_values_callable), nullable=False, default=TransactionType.BAN)
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType, values_callable=_values_callable), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    commission_type: Mapped[CommissionType] = mapped_column(Enum(CommissionType, values_callable=_values_callable), nullable=False)
    commission_value: Mapped[Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    area_width: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    area_length: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_area: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    num_rooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    num_bathrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    num_floors: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    street_name: Mapped[str] = mapped_column(String(255), nullable=False)
    house_number: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    ward: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="Hồ Chí Minh")
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(11, 8), nullable=True)
    label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    furnishing: Mapped[str | None] = mapped_column(String(500), nullable=True)
    frontage_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    legal_status: Mapped[str | None] = mapped_column(String(500), nullable=True)
    direction: Mapped[str | None] = mapped_column(String(50), nullable=True)
    road_width: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owner_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[ListingStatus] = mapped_column(Enum(ListingStatus, values_callable=_values_callable), nullable=False, default=ListingStatus.DRAFT)
    is_hot: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    hot_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    view_count: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
