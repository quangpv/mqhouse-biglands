import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import entity_to_response
from src.modules.reviews.schemas import ReviewResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def get_review_detail(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    review_id: uuid.UUID = Path(..., alias="review_id"),
    repo: ReviewRepo = Depends(ReviewRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ReviewResponse:
    entity = await repo.get(review_id)
    if entity is None or entity.property_id != property_id:
        raise NotFoundError("Review not found")
    return entity_to_response(entity)
