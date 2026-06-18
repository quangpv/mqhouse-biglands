import uuid

from fastapi import Depends, HTTPException, status
from fastapi.responses import Response

from src.data.entities.user import UserEntity
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.listing_repo import ListingRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def delete_image(
    listing_id: uuid.UUID,
    image_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> Response:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can delete images")

    image = await image_repo.get(image_id)
    if image is None or image.listing_id != listing_id:
        raise NotFoundError("Image not found")

    await image_repo.delete(image)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
