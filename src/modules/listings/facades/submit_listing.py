import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError
from src.shared.utils.status_machine import validate_transition


async def submit_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> ListingResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can submit")

    validate_transition(listing.status, ListingStatus.PENDING_APPROVAL)

    image_count = await image_repo.count_by_listing(listing_id)
    if image_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one image is required before submitting")

    listing.status = ListingStatus.PENDING_APPROVAL
    listing = await repo.save(listing)
    return listing_to_response(listing)
