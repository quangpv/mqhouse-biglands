import uuid

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data.entities.review import ReviewEntity
from src.data.entities.review_file import ReviewFileEntity
from src.data.repositories.file_repo import FileRepo
from src.platform.dependencies import get_db


class ReviewRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    _BASE_LOADS = (
        joinedload(ReviewEntity.author),
        joinedload(ReviewEntity.images).joinedload(ReviewFileEntity.file),
    )

    async def get(self, review_id: uuid.UUID) -> ReviewEntity | None:
        result = await self.db.execute(
            select(ReviewEntity)
            .options(*self._BASE_LOADS)
            .where(ReviewEntity.id == review_id)
        )
        return result.unique().scalar_one_or_none()

    async def list_by_property(
        self, property_id: uuid.UUID, page: int = 1, size: int = 20,
    ) -> tuple[list[ReviewEntity], int]:
        condition = ReviewEntity.property_id == property_id

        count_result = await self.db.execute(
            select(func.count()).select_from(ReviewEntity).where(condition)
        )
        total = count_result.scalar() or 0

        result = await self.db.execute(
            select(ReviewEntity)
            .options(*self._BASE_LOADS)
            .where(condition)
            .order_by(ReviewEntity.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        rows = list(result.unique().scalars().all())
        return rows, total

    async def get_by_author_and_property(
        self, author_id: uuid.UUID, property_id: uuid.UUID,
    ) -> ReviewEntity | None:
        result = await self.db.execute(
            select(ReviewEntity).where(
                ReviewEntity.author_id == author_id,
                ReviewEntity.property_id == property_id,
            )
        )
        return result.scalar_one_or_none()

    async def save(self, entity: ReviewEntity) -> ReviewEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def add_images(self, review_id: uuid.UUID, file_ids: list[uuid.UUID]) -> None:
        file_repo = FileRepo(db=self.db)
        for file_id in file_ids:
            file_entity = await file_repo.get(file_id)
            if file_entity is not None:
                rf = ReviewFileEntity(review_id=review_id, file_id=file_id)
                self.db.add(rf)
        await self.db.flush()

    async def delete(self, entity: ReviewEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()
