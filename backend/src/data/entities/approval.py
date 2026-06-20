import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, UUIDMixin

_values_callable = lambda x: [e.value for e in x]  # noqa: E731


class ApprovalType(PyEnum):
    LISTING_POST = "LISTING_POST"
    DEPOSIT = "DEPOSIT"
    CANCELLATION = "CANCELLATION"
    CLOSURE = "CLOSURE"
    SOLD_OUT = "SOLD_OUT"


class DecisionType(PyEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalEntity(Base, UUIDMixin):
    __tablename__ = "approvals"

    listing_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    approval_type: Mapped[ApprovalType] = mapped_column(Enum(ApprovalType, values_callable=_values_callable), nullable=False)
    decision: Mapped[DecisionType] = mapped_column(Enum(DecisionType, values_callable=_values_callable), nullable=False)
    decided_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
