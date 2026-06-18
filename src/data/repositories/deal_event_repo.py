import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.platform.dependencies import get_db


class DealEventRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_listing(self, listing_id: uuid.UUID) -> list[DealEventEntity]:
        result = await self.db.execute(
            select(DealEventEntity)
            .where(DealEventEntity.listing_id == listing_id)
            .order_by(DealEventEntity.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_pending_confirmation(self, listing_id: uuid.UUID, event_type: DealEventType) -> DealEventEntity | None:
        result = await self.db.execute(
            select(DealEventEntity).where(
                DealEventEntity.listing_id == listing_id,
                DealEventEntity.event_type == event_type,
                DealEventEntity.confirmed_by_id.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def has_active_deposit(self, listing_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            select(DealEventEntity).where(
                DealEventEntity.listing_id == listing_id,
                DealEventEntity.event_type == DealEventType.DEPOSIT_REPORTED,
                DealEventEntity.confirmed_by_id.is_(None),
            )
        )
        return result.scalar_one_or_none() is not None

    async def create(self, event: DealEventEntity) -> DealEventEntity:
        self.db.add(event)
        await self.db.flush()
        return event

    async def save(self, event: DealEventEntity) -> DealEventEntity:
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event
