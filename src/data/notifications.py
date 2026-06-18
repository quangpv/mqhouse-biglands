import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity, ReferenceType
from src.data.entities.user import UserEntity

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


async def send_notification(
    db: AsyncSession,
    user_id: uuid.UUID,
    event_type: str,
    title: str,
    body: str,
    reference_type: ReferenceType | None = None,
    reference_id: uuid.UUID | None = None,
) -> NotificationEntity | None:
    result = await db.execute(select(UserEntity).where(UserEntity.id == user_id))
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
    db.add(notification)
    await db.flush()
    return notification
