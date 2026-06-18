import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user_pin import UserPinEntity
from src.platform.dependencies import get_db


class UserPinRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_user_and_listing(self, user_id: uuid.UUID, listing_id: uuid.UUID) -> UserPinEntity | None:
        result = await self.db.execute(
            select(UserPinEntity).where(
                UserPinEntity.user_id == user_id,
                UserPinEntity.listing_id == listing_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: uuid.UUID) -> list[UserPinEntity]:
        result = await self.db.execute(
            select(UserPinEntity)
            .where(UserPinEntity.user_id == user_id)
            .order_by(UserPinEntity.pinned_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, pin: UserPinEntity) -> UserPinEntity:
        self.db.add(pin)
        await self.db.flush()
        return pin

    async def delete(self, pin: UserPinEntity) -> None:
        await self.db.delete(pin)
        await self.db.flush()
