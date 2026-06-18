import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def unpromote_from_hot(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    listing_repo: ListingRepo = Depends(ListingRepo),
) -> HotListingResponse:
    listing = await listing_repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    listing.is_hot = False
    listing.hot_order = None
    listing = await listing_repo.save(listing)

    return listing_to_hot_response(listing)
