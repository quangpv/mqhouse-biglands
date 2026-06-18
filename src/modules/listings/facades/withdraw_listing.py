import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError
from src.shared.utils.status_machine import validate_transition


async def withdraw_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
) -> ListingResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can withdraw")

    validate_transition(listing.status, ListingStatus.DRAFT)

    listing.status = ListingStatus.DRAFT
    listing = await repo.save(listing)
    return listing_to_response(listing)
