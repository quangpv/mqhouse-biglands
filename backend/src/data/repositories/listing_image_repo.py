import uuid

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing_image import ListingImageEntity
from src.platform.dependencies import get_db


from src.data.repositories._base import Repo


class ListingImageRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, image_id: uuid.UUID) -> ListingImageEntity | None:
        result = await self.db.execute(select(ListingImageEntity).where(ListingImageEntity.id == image_id))
        return result.scalar_one_or_none()

    async def list_by_listing(self, listing_id: uuid.UUID) -> list[ListingImageEntity]:
        result = await self.db.execute(
            select(ListingImageEntity)
            .where(ListingImageEntity.listing_id == listing_id)
            .order_by(ListingImageEntity.order)
        )
        return list(result.scalars().all())

    async def count_by_listing(self, listing_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(ListingImageEntity).where(ListingImageEntity.listing_id == listing_id)
        )
        return result.scalar() or 0

    async def create(self, image: ListingImageEntity) -> ListingImageEntity:
        self.db.add(image)
        await self.db.flush()
        return image

    async def delete(self, image: ListingImageEntity) -> None:
        await self.db.delete(image)
        await self.db.flush()

    async def clear_primary(self, listing_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(ListingImageEntity).where(
                ListingImageEntity.listing_id == listing_id,
                ListingImageEntity.is_primary.is_(True),
            )
        )
        for img in result.scalars().all():
            img.is_primary = False
        await self.db.flush()
