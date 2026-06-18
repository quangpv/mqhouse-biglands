import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.token_blacklist import TokenBlacklistEntity
from src.platform.dependencies import get_db


class TokenBlacklistRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add(self, jti: str, expires_at) -> TokenBlacklistEntity:
        entry = TokenBlacklistEntity(jti=jti, expires_at=expires_at)
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def is_blacklisted(self, jti: str) -> bool:
        result = await self.db.execute(
            select(TokenBlacklistEntity).where(TokenBlacklistEntity.jti == jti)
        )
        return result.scalar_one_or_none() is not None
