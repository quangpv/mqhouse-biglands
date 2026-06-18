import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_pin_repo import UserPinRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def unpin_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    listing_repo: ListingRepo = Depends(ListingRepo),
    pin_repo: UserPinRepo = Depends(UserPinRepo),
) -> None:
    listing = await listing_repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    existing = await pin_repo.get_by_user_and_listing(current_user.id, listing_id)
    if existing is not None:
        await pin_repo.delete(existing)
