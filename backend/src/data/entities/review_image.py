from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.review import ReviewEntity


class ReviewImageEntity(Base, UUIDMixin):
    __tablename__ = "review_images"

    review_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    review: Mapped[ReviewEntity] = relationship("ReviewEntity", back_populates="images")
