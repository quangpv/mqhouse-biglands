import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.review import ReviewEntity
from src.data.entities.review_image import ReviewImageEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class ReviewRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, review_id: uuid.UUID) -> ReviewEntity | None:
        result = await self.db.execute(
            select(ReviewEntity)
            .options(selectinload(ReviewEntity.images))
            .where(ReviewEntity.id == review_id)
        )
        return result.scalar_one_or_none()

    async def list_by_listing(
        self, listing_id: uuid.UUID, page: int = 1, size: int = 20
    ) -> tuple[list[ReviewEntity], int]:
        query = (
            select(ReviewEntity)
            .options(selectinload(ReviewEntity.images))
            .where(ReviewEntity.listing_id == listing_id)
            .order_by(ReviewEntity.created_at.desc())
        )
        return await self.paginated_list(query, page=page, size=size)

    async def get_by_author_and_listing(
        self, author_id: uuid.UUID, listing_id: uuid.UUID
    ) -> ReviewEntity | None:
        result = await self.db.execute(
            select(ReviewEntity).where(
                ReviewEntity.author_id == author_id,
                ReviewEntity.listing_id == listing_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, review: ReviewEntity) -> ReviewEntity:
        self.db.add(review)
        await self.db.flush()
        return review

    async def delete(self, review_id: uuid.UUID) -> None:
        review = await self.get(review_id)
        if review:
            await self.db.delete(review)
            await self.db.flush()

    async def count_images_by_review(self, review_id: uuid.UUID) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count()).select_from(ReviewImageEntity).where(ReviewImageEntity.review_id == review_id)
        )
        return result.scalar() or 0

    async def add_image(self, image: ReviewImageEntity) -> ReviewImageEntity:
        self.db.add(image)
        await self.db.flush()
        return image
