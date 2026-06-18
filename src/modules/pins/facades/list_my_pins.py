from math import ceil

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity
from src.data.entities.user import UserEntity
from src.data.entities.user_pin import UserPinEntity
from src.modules.pins.mapper import pinned_listing_to_response
from src.modules.pins.schemas import PinnedListingListResponse, PinnedListingResponse
from src.platform.auth import get_current_user
from src.platform.dependencies import get_db


async def list_my_pins(
    page: int = 1,
    per_page: int = 20,
    current_user: UserEntity = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PinnedListingListResponse:
    count_result = await db.execute(
        select(UserPinEntity).where(UserPinEntity.user_id == current_user.id)
    )
    total = len(count_result.scalars().all())

    query = (
        select(ListingEntity)
        .join(UserPinEntity, UserPinEntity.listing_id == ListingEntity.id)
        .where(UserPinEntity.user_id == current_user.id)
        .order_by(UserPinEntity.pinned_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(query)
    listings = list(result.scalars().all())

    return PinnedListingListResponse(
        data=[pinned_listing_to_response(l) for l in listings],
        total=total,
        page=page,
        size=per_page,
        total_pages=ceil(total / per_page) if per_page > 0 else 0,
    )
