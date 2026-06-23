import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.file import FileEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class FileRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, file_id: uuid.UUID) -> FileEntity | None:
        result = await self.db.execute(
            select(FileEntity).where(FileEntity.id == file_id)
        )
        return result.scalar_one_or_none()

    async def save(self, entity: FileEntity) -> FileEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: FileEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()

    async def get_all_paths(self) -> list[tuple[uuid.UUID, str]]:
        result = await self.db.execute(
            select(FileEntity.id, FileEntity.path)
        )
        return [(r[0], r[1]) for r in result.all()]

    async def get_all_ids(self) -> list[uuid.UUID]:
        result = await self.db.execute(select(FileEntity.id))
        return [row[0] for row in result.all()]
