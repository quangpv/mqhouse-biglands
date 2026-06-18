import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingResponse, UpdateListingRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError

REAPPROVAL_FIELDS = {"price", "area_width", "area_length", "total_area"}


async def update_listing(
    listing_id: uuid.UUID,
    data: UpdateListingRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
) -> ListingResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can edit")

    update_data = data.model_dump(exclude_unset=True)

    if listing.status == ListingStatus.CON_HANG:
        changed_fields = set(update_data.keys())
        if changed_fields & REAPPROVAL_FIELDS:
            listing.status = ListingStatus.PENDING_APPROVAL

    for field, value in update_data.items():
        setattr(listing, field, value)

    listing = await repo.save(listing)
    return listing_to_response(listing)
