from fastapi import APIRouter, Depends, status

from src.modules.pins.facades.list_my_pins import list_my_pins
from src.modules.pins.facades.pin_listing import pin_listing
from src.modules.pins.facades.unpin_listing import unpin_listing
from src.modules.pins.schemas import PinnedListingListResponse, PinnedListingResponse
from src.platform.auth import require_role

router = APIRouter(tags=["pins"])


@router.put("/listings/{listing_id}/pin", response_model=PinnedListingResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def pin(result: PinnedListingResponse = Depends(pin_listing)):
    return result


@router.delete("/listings/{listing_id}/pin", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def unpin(result=Depends(unpin_listing)):
    return result


@router.get("/users/me/pins", response_model=PinnedListingListResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def my_pins(result: PinnedListingListResponse = Depends(list_my_pins)):
    return result
