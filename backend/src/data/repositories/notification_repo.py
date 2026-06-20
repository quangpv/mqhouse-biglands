import uuid

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity, ReferenceType
from src.data.entities.user import UserEntity
from src.platform.dependencies import get_db


from src.data.repositories._base import Repo


DEFAULT_PREFS = {
    "listing_post_created": True,
    "listing_post_approved": True,
    "listing_post_rejected": True,
    "deposit_reported": True,
    "deposit_confirmed": True,
    "deposit_rejected": True,
    "closure_reported": True,
    "closure_confirmed": True,
    "closure_rejected": True,
    "cancellation_reported": True,
    "cancellation_confirmed": True,
    "cancellation_rejected": True,
    "sold_out_reported": True,
    "sold_out_confirmed": True,
    "listing_expired": True,
}

EVENT_TYPE_MAP = {
    "listing_post_created": "LISTING_POST_CREATED",
    "listing_post_approved": "LISTING_POST_APPROVED",
    "listing_post_rejected": "LISTING_POST_REJECTED",
    "deposit_reported": "DEPOSIT_REPORTED",
    "deposit_confirmed": "DEPOSIT_CONFIRMED",
    "deposit_rejected": "DEPOSIT_REJECTED",
    "closure_reported": "CLOSURE_REPORTED",
    "closure_confirmed": "CLOSURE_CONFIRMED",
    "closure_rejected": "CLOSURE_REJECTED",
    "cancellation_reported": "CANCELLATION_REPORTED",
    "cancellation_confirmed": "CANCELLATION_CONFIRMED",
    "cancellation_rejected": "CANCELLATION_REJECTED",
    "sold_out_reported": "SOLD_OUT_REPORTED",
    "sold_out_confirmed": "SOLD_OUT_CONFIRMED",
    "listing_expired": "LISTING_EXPIRED",
}


class NotificationRepo(Repo):
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

    async def send(
        self,
        user_id: uuid.UUID,
        event_type: str,
        title: str,
        body: str,
        reference_type: ReferenceType | None = None,
        reference_id: uuid.UUID | None = None,
    ) -> NotificationEntity | None:
        result = await self.db.execute(select(UserEntity).where(UserEntity.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None

        prefs = user.notification_prefs or DEFAULT_PREFS
        if not prefs.get(event_type, True):
            return None

        notification = NotificationEntity(
            user_id=user_id,
            title=title,
            body=body,
            reference_type=reference_type,
            reference_id=reference_id,
        )
        self.db.add(notification)
        await self.db.flush()
        return notification
