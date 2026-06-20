import uuid

from fastapi import Depends

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse
from src.platform.auth import get_current_user
from src.platform.config import settings
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def promote_to_hot(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    listing_repo: ListingRepo = Depends(ListingRepo),
) -> HotListingResponse:
    listing = await listing_repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.CON_HANG:
        raise ConflictError(detail="Only CON_HANG listings can be promoted")
    if listing.is_hot:
        return listing_to_hot_response(listing)

    hot_count = await listing_repo.count_hot_listings()
    if hot_count >= settings.max_hot_items:
        raise ConflictError(detail=f"Maximum {settings.max_hot_items} hot listings allowed")

    listing.is_hot = True
    listing.hot_order = hot_count + 1
    listing = await listing_repo.save(listing)

    return listing_to_hot_response(listing)
