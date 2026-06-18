import uuid

from fastapi import Depends
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity, ReferenceType
from src.platform.dependencies import get_db


class NotificationRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def list_by_user(
        self, user_id: uuid.UUID, page: int, per_page: int, is_read: bool | None = None
    ) -> tuple[list[NotificationEntity], int]:
        query = select(NotificationEntity).where(NotificationEntity.user_id == user_id)
        count_query = select(func.count(NotificationEntity.id)).where(NotificationEntity.user_id == user_id)
        if is_read is not None:
            query = query.where(NotificationEntity.is_read == is_read)
            count_query = count_query.where(NotificationEntity.is_read == is_read)
        query = query.order_by(NotificationEntity.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)

        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        result = await self.db.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_unread_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(NotificationEntity.id)).where(
                NotificationEntity.user_id == user_id,
                NotificationEntity.is_read.is_(False),
            )
        )
        return result.scalar_one()

    async def get_by_id(self, notification_id: uuid.UUID) -> NotificationEntity | None:
        result = await self.db.execute(
            select(NotificationEntity).where(NotificationEntity.id == notification_id)
        )
        return result.scalar_one_or_none()

    async def mark_read(self, notification_id: uuid.UUID) -> NotificationEntity | None:
        notification = await self.get_by_id(notification_id)
        if notification is None:
            return None
        notification.is_read = True
        await self.db.flush()
        return notification

    async def mark_all_read(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(NotificationEntity).where(
                NotificationEntity.user_id == user_id,
                NotificationEntity.is_read.is_(False),
            )
        )
        pending = result.scalars().all()
        for n in pending:
            n.is_read = True
        await self.db.flush()
        return len(pending)

    async def create(self, notification: NotificationEntity) -> NotificationEntity:
        self.db.add(notification)
        await self.db.flush()
        return notification
