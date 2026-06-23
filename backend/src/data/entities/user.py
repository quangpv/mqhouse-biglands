import uuid
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.data.entities.organization import OrganizationEntity


def _values_callable(x):
    return [e.value for e in x]


class UserRole(PyEnum):
    SALE = "SALE"
    APPROVER = "APPROVER"
    ADMIN = "ADMIN"


class UserEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"
    __allow_unmapped__ = True

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

    device_limit_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    device_id: Mapped[str | None] = mapped_column(String(500), nullable=True)

    transaction_types: Mapped[list["UserTransactionTypeEntity"]] = relationship(
        "UserTransactionTypeEntity",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    property_types: Mapped[list["UserPropertyTypeEntity"]] = relationship(
        "UserPropertyTypeEntity",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    _raw_token: str | None = None
    _jti: str | None = None
    _exp: int | None = None


class UserTransactionTypeEntity(Base):
    __tablename__ = "user_transaction_types"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    transaction_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transaction_types.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["UserEntity"] = relationship(back_populates="transaction_types")


class UserPropertyTypeEntity(Base):
    __tablename__ = "user_property_types"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    property_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_types.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["UserEntity"] = relationship(back_populates="property_types")
