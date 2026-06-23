import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.data.entities.hot_property import HotPropertyEntity
from src.data.entities.property import PropertyEntity
from src.data.entities.property_image import PropertyImageEntity
from src.data.repositories._base import Repo


class HotPropertyRepo(Repo):
    _PROPERTY_LOADS = (
        joinedload(HotPropertyEntity.property).joinedload(PropertyEntity.creator),
        joinedload(HotPropertyEntity.property).joinedload(PropertyEntity.transaction_type),
        joinedload(HotPropertyEntity.property).joinedload(PropertyEntity.property_type),
        joinedload(HotPropertyEntity.property)
        .selectinload(PropertyEntity.images)
        .selectinload(PropertyImageEntity.file),
    )

    async def list_active(self) -> list[HotPropertyEntity]:
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(HotPropertyEntity)
            .options(*self._PROPERTY_LOADS)
            .where(
                HotPropertyEntity.start_time <= now,
                HotPropertyEntity.end_time > now,
            )
            .order_by(HotPropertyEntity.start_time.desc())
        )
        return list(result.unique().scalars().all())

    async def get_by_property(self, property_id: uuid.UUID) -> HotPropertyEntity | None:
        result = await self.db.execute(
            select(HotPropertyEntity).options(*self._PROPERTY_LOADS).where(HotPropertyEntity.property_id == property_id)
        )
        return result.unique().scalar_one_or_none()

    async def save(self, entity: HotPropertyEntity) -> HotPropertyEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: HotPropertyEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()
