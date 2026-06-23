import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.transaction_type import TransactionTypeEntity
from src.platform.dependencies import get_db


class TransactionTypeRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, entity_id: uuid.UUID) -> TransactionTypeEntity | None:
        result = await self.db.execute(
            select(TransactionTypeEntity).where(TransactionTypeEntity.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> TransactionTypeEntity | None:
        result = await self.db.execute(
            select(TransactionTypeEntity).where(TransactionTypeEntity.code == code)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[TransactionTypeEntity]:
        result = await self.db.execute(
            select(TransactionTypeEntity).order_by(TransactionTypeEntity.code)
        )
        return list(result.scalars().all())

    async def save(self, entity: TransactionTypeEntity) -> TransactionTypeEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: TransactionTypeEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()
