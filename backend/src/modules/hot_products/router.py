from fastapi import APIRouter, Depends

from src.modules.hot_products.facades.get_hot_listings import get_hot_listings
from src.modules.hot_products.facades.promote_to_hot import promote_to_hot
from src.modules.hot_products.facades.reorder_hot_listings import reorder_hot_listings
from src.modules.hot_products.facades.unpromote_from_hot import unpromote_from_hot
from src.modules.hot_products.schemas import HotListingResponse
from src.platform.auth import require_role

router = APIRouter(tags=["hot_products"])


@router.post("/listings/{listing_id}/promote", response_model=HotListingResponse, dependencies=[Depends(require_role("ADMIN"))])
async def promote(result: HotListingResponse = Depends(promote_to_hot)):
    return result


@router.delete("/listings/{listing_id}/promote", response_model=HotListingResponse, dependencies=[Depends(require_role("ADMIN"))])
async def unpromote(result: HotListingResponse = Depends(unpromote_from_hot)):
    return result


@router.get("/hot-listings", response_model=list[HotListingResponse])
async def hot_list(result: list[HotListingResponse] = Depends(get_hot_listings)):
    return result


@router.put("/hot-listings/reorder", response_model=list[HotListingResponse], dependencies=[Depends(require_role("ADMIN"))])
async def reorder(result: list[HotListingResponse] = Depends(reorder_hot_listings)):
    return result
