import os
import uuid

from fastapi import Depends, UploadFile

from src.data.entities.review_image import ReviewImageEntity
from src.data.entities.user import UserEntity
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import review_image_to_response
from src.modules.reviews.schemas import ReviewImageResponse
from src.platform.auth import get_current_user
from src.platform.config import settings
from src.shared.errors.exceptions import BadRequestError, ForbiddenError, NotFoundError


async def upload_review_image(
    listing_id: uuid.UUID,
    review_id: uuid.UUID,
    file: UploadFile,
    current_user: UserEntity = Depends(get_current_user),
    repo: ReviewRepo = Depends(ReviewRepo),
) -> ReviewImageResponse:
    review = await repo.get(review_id)
    if review is None:
        raise NotFoundError("Review not found")

    if review.listing_id != listing_id:
        raise NotFoundError("Review not found for this listing")

    if review.author_id != current_user.id:
        raise ForbiddenError("Only the review author can upload images")

    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise BadRequestError("Only JPEG, PNG, and WEBP files are allowed")

    contents = await file.read()
    if len(contents) > settings.max_upload_size_mb * 1024 * 1024:
        raise BadRequestError(f"File exceeds {settings.max_upload_size_mb}MB limit")

    image_count = await repo.count_images_by_review(review_id)
    if image_count >= 10:
        raise BadRequestError("Maximum 10 images per review")

    filename = file.filename or "image.jpg"
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.upload_dir, filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    image = ReviewImageEntity(
        review_id=review_id,
        url=f"/uploads/{filename}",
        order=image_count + 1,
    )
    image = await repo.add_image(image)
    return review_image_to_response(image)
