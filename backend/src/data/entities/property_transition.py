import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, UUIDMixin
from src.data.entities.property import Action, PropertyStatus

if TYPE_CHECKING:
    from src.data.entities.property import PropertyEntity
    from src.data.entities.user import UserEntity
    from src.data.entities.transition_file import TransitionFileEntity


def _values_callable(x):
    return [e.value for e in x]


class PropertyTransitionEntity(Base, UUIDMixin):
    __tablename__ = "property_transitions"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    from_status: Mapped[PropertyStatus | None] = mapped_column(
        Enum(PropertyStatus, values_callable=_values_callable), nullable=True
    )
    to_status: Mapped[PropertyStatus] = mapped_column(
        Enum(PropertyStatus, values_callable=_values_callable), nullable=False
    )
    action: Mapped[Action] = mapped_column(
        Enum(Action, values_callable=_values_callable), nullable=False
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    actor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    customer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    customer_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contract_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    property: Mapped["PropertyEntity"] = relationship(back_populates="transitions")  # type: ignore
    actor: Mapped["UserEntity"] = relationship("UserEntity", lazy="selectin")  # type: ignore
    files: Mapped[list["TransitionFileEntity"]] = relationship(
        "TransitionFileEntity",
        back_populates="transition",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
