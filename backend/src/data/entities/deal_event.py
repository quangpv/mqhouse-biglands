import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, UUIDMixin

_values_callable = lambda x: [e.value for e in x]  # noqa: E731


class DealEventType(PyEnum):
    DEPOSIT_REPORTED = "DEPOSIT_REPORTED"
    DEPOSIT_CONFIRMED = "DEPOSIT_CONFIRMED"
    CLOSURE_REPORTED = "CLOSURE_REPORTED"
    CLOSURE_CONFIRMED = "CLOSURE_CONFIRMED"
    CANCELLATION_REPORTED = "CANCELLATION_REPORTED"
    CANCELLATION_CONFIRMED = "CANCELLATION_CONFIRMED"
    SOLD_OUT_REPORTED = "SOLD_OUT_REPORTED"
    SOLD_OUT_CONFIRMED = "SOLD_OUT_CONFIRMED"


class DealEventEntity(Base, UUIDMixin):
    __tablename__ = "deal_events"

    listing_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[DealEventType] = mapped_column(Enum(DealEventType, values_callable=_values_callable), nullable=False)
    reported_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    confirmed_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    customer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    customer_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    deposit_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 0), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
