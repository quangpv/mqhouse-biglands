import uuid
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.property import PropertyEntity
    from src.data.entities.property_transition import PropertyTransitionEntity
    from src.data.entities.transaction_type import TransactionTypeEntity


def _values_callable(x):
    return [e.value for e in x]


class ApprovalStatus(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "approvals"
    __table_args__ = (Index("ix_approvals_status_created", "status", "created_at"),)

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False
    )
    transition_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_transitions.id"), nullable=True
    )
    transaction_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transaction_types.id"), nullable=False
    )
    status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus, values_callable=_values_callable),
        nullable=False,
        default=ApprovalStatus.PENDING,
    )
    decision_transition_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_transitions.id"), nullable=True
    )
    old_values: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    property: Mapped["PropertyEntity"] = relationship(
        "PropertyEntity", lazy="selectin"
    )
    transition: Mapped["PropertyTransitionEntity | None"] = relationship(
        "PropertyTransitionEntity",
        foreign_keys=[transition_id],
        lazy="selectin",
    )
    decision_transition: Mapped["PropertyTransitionEntity | None"] = relationship(
        "PropertyTransitionEntity",
        foreign_keys=[decision_transition_id],
        lazy="selectin",
    )
    transaction_type: Mapped["TransactionTypeEntity"] = relationship(
        "TransactionTypeEntity", lazy="selectin"
    )
