import uuid
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

_values_callable = lambda x: [e.value for e in x]  # noqa: E731


class UserRole(PyEnum):
    SALE = "SALE"
    APPROVER = "APPROVER"
    ADMIN = "ADMIN"


class UserEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, values_callable=_values_callable), nullable=False,
                                           default=UserRole.SALE)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"),
                                                               nullable=True)
    organization: Mapped["OrganizationEntity | None"] = relationship("OrganizationEntity", lazy="selectin")

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
