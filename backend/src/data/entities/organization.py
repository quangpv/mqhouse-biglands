from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, TimestampMixin, UUIDMixin


class OrganizationEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
