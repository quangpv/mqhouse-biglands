import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.property_image import PropertyImageEntity
    from src.data.entities.property_transition import PropertyTransitionEntity
    from src.data.entities.property_type import PropertyTypeEntity
    from src.data.entities.review import ReviewEntity
    from src.data.entities.transaction_type import TransactionTypeEntity
    from src.data.entities.user import UserEntity


def _values_callable(x):
    return [e.value for e in x]


class CommissionType(PyEnum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"


class DirectionType(PyEnum):
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"
    NORTH = "NORTH"
    NORTHEAST = "NORTHEAST"
    SOUTHEAST = "SOUTHEAST"
    NORTHWEST = "NORTHWEST"
    SOUTHWEST = "SOUTHWEST"


class PropertyStatus(PyEnum):
    DRAFT = "draft"
    POST_PENDING = "post_pending"
    EDIT_PENDING = "edit_pending"
    DEPOSIT_PENDING = "deposit_pending"
    SOLDOUT_PENDING = "soldout_pending"
    COMPLETE_PENDING = "complete_pending"
    CANCEL_PENDING = "cancel_pending"
    AVAILABLE = "available"
    DEPOSITED = "deposited"
    SOLDOUT = "soldout"
    EXPIRED = "expired"
    COMPLETED = "completed"


class Action(PyEnum):
    SUBMIT = "submit"
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    SOLDOUT = "soldout"
    CANCEL = "cancel"
    COMPLETE = "complete"
    EDIT = "edit"
    APPROVE = "approve"
    REJECT = "reject"


class PropertyEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "properties"

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    transaction_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transaction_types.id"), nullable=False
    )
    property_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_types.id"), nullable=False
    )

    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    commission_type: Mapped[CommissionType] = mapped_column(
        Enum(CommissionType, values_callable=_values_callable), nullable=False
    )
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
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(11, 8), nullable=True)

    label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    furnishing: Mapped[str | None] = mapped_column(String(500), nullable=True)
    frontage_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    legal_status: Mapped[str | None] = mapped_column(String(500), nullable=True)
    direction: Mapped[DirectionType | None] = mapped_column(
        Enum(DirectionType, values_callable=_values_callable), nullable=True
    )
    road_width: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owner_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[PropertyStatus] = mapped_column(
        Enum(PropertyStatus, values_callable=_values_callable), nullable=False, default=PropertyStatus.DRAFT
    )
    is_hot: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    hot_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    transaction_type: Mapped["TransactionTypeEntity"] = relationship(  # type: ignore
        "TransactionTypeEntity", lazy="selectin"
    )
    property_type: Mapped["PropertyTypeEntity"] = relationship(  # type: ignore
        "PropertyTypeEntity", lazy="selectin"
    )
    creator: Mapped["UserEntity"] = relationship(  # type: ignore
        "UserEntity", foreign_keys=[created_by_id], lazy="selectin"
    )

    images: Mapped[list["PropertyImageEntity"]] = relationship(
        "PropertyImageEntity",
        back_populates="property",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    transitions: Mapped[list["PropertyTransitionEntity"]] = relationship(
        "PropertyTransitionEntity",
        back_populates="property",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="PropertyTransitionEntity.created_at",
    )
    reviews: Mapped[list["ReviewEntity"]] = relationship(  # type: ignore
        "ReviewEntity",
        back_populates="property",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
