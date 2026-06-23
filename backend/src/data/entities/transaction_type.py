from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, TimestampMixin, UUIDMixin


class TransactionTypeEntity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "transaction_types"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
