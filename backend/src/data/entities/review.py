import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.review_file import ReviewFileEntity
    from src.data.entities.property import PropertyEntity
    from src.data.entities.user import UserEntity


class ReviewEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    property: Mapped["PropertyEntity"] = relationship(back_populates="reviews")
    author: Mapped["UserEntity"] = relationship("UserEntity", lazy="selectin")
    images: Mapped[list["ReviewFileEntity"]] = relationship(
        "ReviewFileEntity",
        back_populates="review",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
