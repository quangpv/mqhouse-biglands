import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, UUIDMixin


class ListingImageEntity(Base, UUIDMixin):
    __tablename__ = "listing_images"

    listing_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_primary: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
