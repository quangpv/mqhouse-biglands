from fastapi import Depends

from src.data.repositories.listing_repo import ListingRepo
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse, ReorderHotListingsRequest
from src.shared.errors.exceptions import BadRequestError, NotFoundError


async def reorder_hot_listings(
    data: ReorderHotListingsRequest,
    listing_repo: ListingRepo = Depends(ListingRepo),
) -> list[HotListingResponse]:
    existing_hot = await listing_repo.get_hot_listing_ids()
    submitted_ids = set(data.listing_ids)

    if not submitted_ids.issubset(existing_hot):
        raise BadRequestError("All listing_ids must be currently promoted hot listings")

    if len(data.listing_ids) != len(set(data.listing_ids)):
        raise BadRequestError("Duplicate listing_ids are not allowed")

    listings = await listing_repo.get_by_ids(data.listing_ids)
    listing_map = {listing.id: listing for listing in listings}

    updated = []
    for idx, lid in enumerate(data.listing_ids):
        listing = listing_map.get(lid)
        if listing is None:
            raise NotFoundError(f"Listing {lid} not found")
        listing.hot_order = idx + 1
        updated.append(listing)

    for listing in updated:
        listing = await listing_repo.save(listing)

    return [listing_to_hot_response(listing) for listing in updated]
