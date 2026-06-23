import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.file import FileEntity
    from src.data.entities.review import ReviewEntity


class ReviewFileEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "review_files"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), nullable=False
    )

    review: Mapped["ReviewEntity"] = relationship(back_populates="images")  # type: ignore
    file: Mapped["FileEntity"] = relationship("FileEntity", lazy="selectin")  # type: ignore
