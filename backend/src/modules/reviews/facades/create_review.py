import uuid

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.data.entities.review import ReviewEntity
from src.data.entities.user import UserEntity
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import review_to_response
from src.modules.reviews.schemas import CreateReviewRequest, ReviewResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError


async def create_review(
    listing_id: uuid.UUID,
    data: CreateReviewRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ReviewRepo = Depends(ReviewRepo),
) -> ReviewResponse:
    existing = await repo.get_by_author_and_listing(current_user.id, listing_id)
    if existing:
        raise ConflictError("You have already reviewed this listing")

    review = ReviewEntity(
        listing_id=listing_id,
        author_id=current_user.id,
        author_name=current_user.full_name,
        content=data.content,
    )
    try:
        review = await repo.create(review)
    except IntegrityError:
        raise ConflictError("You have already reviewed this listing")

    review = await repo.get(review.id)
    return review_to_response(review)
