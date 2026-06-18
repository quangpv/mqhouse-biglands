import uuid

from fastapi import Depends

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, ForbiddenError, NotFoundError


async def delete_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
) -> None:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise ForbiddenError("Only the listing owner can delete")

    if listing.status != ListingStatus.DRAFT:
        raise ConflictError("Only DRAFT listings can be deleted. Withdraw the listing first.")

    await repo.hard_delete(listing_id)
