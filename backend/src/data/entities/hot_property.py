import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.property import PropertyEntity
    from src.data.entities.user import UserEntity


class HotPropertyEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "hot_properties"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    property: Mapped["PropertyEntity"] = relationship("PropertyEntity", lazy="selectin")
    creator: Mapped["UserEntity"] = relationship("UserEntity", lazy="selectin")
