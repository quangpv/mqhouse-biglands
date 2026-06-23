import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.entities._base import Base, TimestampMixin, UUIDMixin


class OrganizationEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)

    transaction_types: Mapped[list["OrgTransactionTypeEntity"]] = relationship(
        "OrgTransactionTypeEntity",
        back_populates="organization",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    property_types: Mapped[list["OrgPropertyTypeEntity"]] = relationship(
        "OrgPropertyTypeEntity",
        back_populates="organization",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class OrgTransactionTypeEntity(Base):
    __tablename__ = "organization_transaction_types"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    transaction_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transaction_types.id", ondelete="CASCADE"), primary_key=True
    )

    organization: Mapped["OrganizationEntity"] = relationship(back_populates="transaction_types")


class OrgPropertyTypeEntity(Base):
    __tablename__ = "organization_property_types"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    property_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_types.id", ondelete="CASCADE"), primary_key=True
    )

    organization: Mapped["OrganizationEntity"] = relationship(back_populates="property_types")
