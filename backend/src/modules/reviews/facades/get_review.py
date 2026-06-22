import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import review_to_response
from src.modules.reviews.schemas import ReviewResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def get_review(
    listing_id: uuid.UUID,
    review_id: uuid.UUID,
    repo: ReviewRepo = Depends(ReviewRepo),
) -> ReviewResponse:
    review = await repo.get(review_id)
    if review is None:
        raise NotFoundError("Review not found")
    return review_to_response(review)


async def delete_review(
    listing_id: uuid.UUID,
    review_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ReviewRepo = Depends(ReviewRepo),
) -> None:
    review = await repo.get(review_id)
    if review is None:
        raise NotFoundError("Review not found")

    if review.author_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Only the author or an admin can delete this review")

    await repo.delete(review_id)
