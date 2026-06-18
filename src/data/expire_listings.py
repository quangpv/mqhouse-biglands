import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.notifications import send_notification
from src.data.repositories.listing_repo import ListingRepo
from src.platform.config import settings
from src.platform.database import async_session_factory

logger = logging.getLogger("biglands.expire_listings")


async def _do_expire(db: AsyncSession) -> int:
    repo = ListingRepo(db)
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.expiration_days)
    expired = await repo.list_expired(cutoff)
    for listing in expired:
        listing.status = ListingStatus.QUA_HAN
        await repo.save(listing)
        await send_notification(
            db=db,
            user_id=listing.created_by_id,
            event_type="listing_expired",
            title=f"Listing {listing.code} đã hết hạn",
            body=f"Your {listing.transaction_type.value} listing {listing.title} has expired after {settings.expiration_days} days",
            reference_type=ReferenceType.LISTING,
            reference_id=listing.id,
        )
        logger.info("Expired listing %s (created_at=%s)", listing.id, listing.created_at)
    await db.commit()
    return len(expired)


async def expire_listings() -> int:
    async with async_session_factory() as db:
        return await _do_expire(db)
