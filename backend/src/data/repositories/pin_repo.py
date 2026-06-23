import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.data.entities.pin import PinEntity
from src.data.entities.property import PropertyEntity
from src.data.entities.property_image import PropertyImageEntity
from src.data.repositories._base import Repo


class PinRepo(Repo):
    _PROPERTY_LOADS = (
        joinedload(PinEntity.property).joinedload(PropertyEntity.creator),
        joinedload(PinEntity.property).joinedload(PropertyEntity.transaction_type),
        joinedload(PinEntity.property).joinedload(PropertyEntity.property_type),
        joinedload(PinEntity.property).selectinload(PropertyEntity.images).selectinload(PropertyImageEntity.file),
    )

    async def get(self, user_id: uuid.UUID, property_id: uuid.UUID) -> PinEntity | None:
        result = await self.db.execute(
            select(PinEntity)
            .options(*self._PROPERTY_LOADS)
            .where(PinEntity.user_id == user_id, PinEntity.property_id == property_id)
        )
        return result.unique().scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[PinEntity], int]:
        condition = PinEntity.user_id == user_id

        count_result = await self.db.execute(select(func.count()).select_from(PinEntity).where(condition))
        total = count_result.scalar() or 0

        result = await self.db.execute(
            select(PinEntity)
            .options(*self._PROPERTY_LOADS)
            .where(condition)
            .order_by(PinEntity.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        rows = list(result.unique().scalars().all())
        return rows, total

    async def save(self, entity: PinEntity) -> PinEntity:
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def delete(self, entity: PinEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()
