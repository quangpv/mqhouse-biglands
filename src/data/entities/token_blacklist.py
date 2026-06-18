import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.data.entities._base import Base, UUIDMixin


class TokenBlacklistEntity(Base, UUIDMixin):
    __tablename__ = "token_blacklist"

    jti: Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
