import uuid

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.notification import NotificationEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class NotificationRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def save(self, entity: NotificationEntity) -> NotificationEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def get(self, notification_id: uuid.UUID) -> NotificationEntity | None:
        result = await self.db.execute(
            select(NotificationEntity).where(NotificationEntity.id == notification_id),
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: uuid.UUID,
        *,
        is_read: bool | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[NotificationEntity], int, int]:
        query = select(NotificationEntity).where(NotificationEntity.user_id == user_id)

        if is_read is not None:
            query = query.where(NotificationEntity.is_read == is_read)

        query = query.order_by(NotificationEntity.created_at.desc())
        return await self.paginated_list(query, page=page, size=size)

    async def unread_count(self, user_id: uuid.UUID) -> int:
        from sqlalchemy import func as sqlfunc

        result = await self.db.execute(
            select(sqlfunc.count(NotificationEntity.id))
            .where(NotificationEntity.user_id == user_id, NotificationEntity.is_read == False),
        )
        return result.scalar() or 0

    async def mark_read(self, notification_id: uuid.UUID) -> NotificationEntity | None:
        result = await self.db.execute(
            update(NotificationEntity)
            .where(NotificationEntity.id == notification_id)
            .values(is_read=True)
            .returning(NotificationEntity),
        )
        return result.scalar_one_or_none()

    async def mark_all_read(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            update(NotificationEntity)
            .where(NotificationEntity.user_id == user_id, NotificationEntity.is_read == False)
            .values(is_read=True)
            .returning(NotificationEntity.id),
        )
        return len(result.all())
