import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.property_type import PropertyTypeEntity
from src.platform.dependencies import get_db


class PropertyTypeRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, entity_id: uuid.UUID) -> PropertyTypeEntity | None:
        result = await self.db.execute(
            select(PropertyTypeEntity).where(PropertyTypeEntity.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> PropertyTypeEntity | None:
        result = await self.db.execute(
            select(PropertyTypeEntity).where(PropertyTypeEntity.code == code)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[PropertyTypeEntity]:
        result = await self.db.execute(
            select(PropertyTypeEntity).order_by(PropertyTypeEntity.code)
        )
        return list(result.scalars().all())

    async def save(self, entity: PropertyTypeEntity) -> PropertyTypeEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: PropertyTypeEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()
