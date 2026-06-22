import uuid

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity
from src.data.entities.user_pin import UserPinEntity
from src.platform.dependencies import get_db


from src.data.repositories._base import Repo


class UserPinRepo(Repo):
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

    async def get_pinned_listing_ids(self, user_id: uuid.UUID, listing_ids: list[uuid.UUID]) -> set[uuid.UUID]:
        if not listing_ids:
            return set()
        result = await self.db.execute(
            select(UserPinEntity.listing_id).where(
                UserPinEntity.user_id == user_id,
                UserPinEntity.listing_id.in_(listing_ids),
            )
        )
        return set(result.scalars().all())

    async def list_by_user(self, user_id: uuid.UUID) -> list[UserPinEntity]:
        result = await self.db.execute(
            select(UserPinEntity)
            .where(UserPinEntity.user_id == user_id)
            .order_by(UserPinEntity.pinned_at.desc())
        )
        return list(result.scalars().all())

    async def count_by_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(UserPinEntity.user_id)).where(UserPinEntity.user_id == user_id)
        )
        return result.scalar_one()

    async def get_pinned_listings_paginated(
        self, user_id: uuid.UUID, page: int, per_page: int
    ) -> list[ListingEntity]:
        result = await self.db.execute(
            select(ListingEntity)
            .join(UserPinEntity, UserPinEntity.listing_id == ListingEntity.id)
            .where(UserPinEntity.user_id == user_id)
            .order_by(UserPinEntity.pinned_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        return list(result.scalars().all())

    async def create(self, pin: UserPinEntity) -> UserPinEntity:
        self.db.add(pin)
        await self.db.flush()
        return pin

    async def delete(self, pin: UserPinEntity) -> None:
        await self.db.delete(pin)
        await self.db.flush()
