import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.user import UserEntity
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listing_images.mapper import image_to_response
from src.modules.listing_images.schemas import ImageResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def set_primary_image(
    listing_id: uuid.UUID,
    image_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> ImageResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can set primary image")

    image = await image_repo.get(image_id)
    if image is None or image.listing_id != listing_id:
        raise NotFoundError("Image not found")

    await image_repo.clear_primary(listing_id)
    image.is_primary = True
    image = await image_repo.create(image)
    return image_to_response(image)
