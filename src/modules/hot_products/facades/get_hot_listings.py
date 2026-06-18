from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse
from src.platform.dependencies import get_db


async def get_hot_listings(
    db: AsyncSession = Depends(get_db),
) -> list[HotListingResponse]:
    result = await db.execute(
        select(ListingEntity)
        .where(ListingEntity.is_hot.is_(True))
        .order_by(ListingEntity.hot_order.asc().nullslast())
    )
    listings = result.scalars().all()
    return [listing_to_hot_response(l) for l in listings]
