import uuid
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, TimestampMixin, UUIDMixin


_values_callable = lambda x: [e.value for e in x]


class EntityType(PyEnum):
    REVIEW = "review"
    PROPERTY = "property"
    AVATAR = "avatar"


class FileEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "files"

    origin_name: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    mimetype: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType, values_callable=_values_callable), nullable=True
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
