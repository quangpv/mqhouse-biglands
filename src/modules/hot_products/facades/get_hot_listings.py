from fastapi import Depends

from src.data.repositories.listing_repo import ListingRepo
from src.modules.hot_products.mapper import listing_to_hot_response
from src.modules.hot_products.schemas import HotListingResponse


async def get_hot_listings(
    listing_repo: ListingRepo = Depends(ListingRepo),
) -> list[HotListingResponse]:
    listings = await listing_repo.get_hot_listings()
    return [listing_to_hot_response(l) for l in listings]
