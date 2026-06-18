from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse, ReorderHotListingsRequest
from src.platform.dependencies import get_db
from src.shared.errors.exceptions import BadRequestError, NotFoundError


async def reorder_hot_listings(
    data: ReorderHotListingsRequest,
    listing_repo: ListingRepo = Depends(ListingRepo),
    db: AsyncSession = Depends(get_db),
) -> list[HotListingResponse]:
    hot_result = await db.execute(
        select(ListingEntity).where(ListingEntity.is_hot.is_(True))
    )
    existing_hot = {str(l.id) for l in hot_result.scalars().all()}
    submitted_ids = {str(lid) for lid in data.listing_ids}

    if not submitted_ids.issubset(existing_hot):
        raise BadRequestError("All listing_ids must be currently promoted hot listings")

    if len(data.listing_ids) != len(set(data.listing_ids)):
        raise BadRequestError("Duplicate listing_ids are not allowed")

    updated = []
    for idx, lid in enumerate(data.listing_ids):
        listing = await listing_repo.get(lid)
        if listing is None:
            raise NotFoundError(f"Listing {lid} not found")
        listing.hot_order = idx + 1
        listing = await listing_repo.save(listing)
        updated.append(listing)

    return [listing_to_hot_response(l) for l in updated]
