import uuid

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin


class ReviewEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    listing_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    images: Mapped[list["ReviewImageEntity"]] = relationship("ReviewImageEntity", back_populates="review", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("author_id", "listing_id", name="uq_review_author_listing"),
    )
