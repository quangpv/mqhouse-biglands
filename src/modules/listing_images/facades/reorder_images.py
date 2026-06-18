import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.user import UserEntity
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listing_images.mapper import image_to_response
from src.modules.listing_images.schemas import ImageResponse, ReorderImagesRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def reorder_images(
    listing_id: uuid.UUID,
    data: ReorderImagesRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> list[ImageResponse]:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can reorder images")

    images = await image_repo.list_by_listing(listing_id)
    image_map = {img.id: img for img in images}

    for idx, img_id in enumerate(data.image_ids, start=1):
        img = image_map.get(img_id)
        if img is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Image {img_id} not found in this listing")
        img.order = idx
        if idx == 1:
            img.is_primary = True
        else:
            img.is_primary = False
        image_repo.db.add(img)

    await image_repo.db.flush()
    result = await image_repo.list_by_listing(listing_id)
    return [image_to_response(img) for img in result]
