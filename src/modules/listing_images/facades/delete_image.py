import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.listing_repo import ListingRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def delete_image(
    listing_id: uuid.UUID,
    image_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> None:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.created_by_id != current_user.id:
        raise ForbiddenError("Only the listing owner can delete images")

    image = await image_repo.get(image_id)
    if image is None or image.listing_id != listing_id:
        raise NotFoundError("Image not found")

    await image_repo.delete(image)
