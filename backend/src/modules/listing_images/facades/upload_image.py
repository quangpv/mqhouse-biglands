import uuid

from fastapi import Depends, UploadFile

from src.data.entities.listing_image import ListingImageEntity
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.modules.listing_images.mapper import image_to_response
from src.modules.listing_images.schemas import ImageResponse
from src.platform.auth import get_current_user
from src.platform.config import settings
from src.shared.errors.exceptions import BadRequestError, ConflictError, ForbiddenError, NotFoundError


async def upload_image(
    listing_id: uuid.UUID,
    file: UploadFile,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
) -> ImageResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.created_by_id != current_user.id:
        raise ForbiddenError("Only the listing owner can upload images")

    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise BadRequestError("Only JPEG, PNG, and WEBP files are allowed")

    contents = await file.read()
    if len(contents) > settings.max_upload_size_mb * 1024 * 1024:
        raise BadRequestError(f"File exceeds {settings.max_upload_size_mb}MB limit")

    count = await image_repo.count_by_listing(listing_id)
    if count >= 20:
        raise ConflictError("Maximum 20 images per listing")

    import os
    os.makedirs(settings.upload_dir, exist_ok=True)

    filename = file.filename or "image.jpg"
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.upload_dir, filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    image = ListingImageEntity(
        listing_id=listing_id,
        url=f"/uploads/{filename}",
        order=count + 1,
        is_primary=count == 0,
    )
    image = await image_repo.create(image)
    return image_to_response(image)
