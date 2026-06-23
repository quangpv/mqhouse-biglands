import uuid
from datetime import datetime

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.refresh_token import RefreshTokenEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class RefreshTokenRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add(self, user_id: uuid.UUID, token_hash: str, expires_at: datetime) -> RefreshTokenEntity:
        entry = RefreshTokenEntity(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def get_by_token_hash(self, token_hash: str) -> RefreshTokenEntity | None:
        result = await self.db.execute(
            select(RefreshTokenEntity).where(RefreshTokenEntity.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke(self, token_id: uuid.UUID) -> None:
        await self.db.execute(
            update(RefreshTokenEntity).where(RefreshTokenEntity.id == token_id).values(is_revoked=True)
        )
        await self.db.flush()

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        await self.db.execute(
            update(RefreshTokenEntity)
            .where(RefreshTokenEntity.user_id == user_id, ~RefreshTokenEntity.is_revoked)
            .values(is_revoked=True)
        )
        await self.db.flush()
