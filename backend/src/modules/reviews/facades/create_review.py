import uuid

from fastapi import Body, Depends, Path

from src.data.entities.user import UserEntity
from src.data.repositories.property_repo import PropertyRepo
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import entity_to_response, request_to_entity
from src.modules.reviews.schemas import CreateReviewRequest, ReviewResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def create_review(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    body: CreateReviewRequest = Body(...),
    repo: ReviewRepo = Depends(ReviewRepo),
    prop_repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ReviewResponse:
    prop = await prop_repo.get(property_id)
    if prop is None:
        raise NotFoundError("Property not found")

    existing = await repo.get_by_author_and_property(current_user.id, property_id)
    if existing is not None:
        raise ConflictError("You have already reviewed this property")

    entity = request_to_entity(body, property_id, current_user.id, current_user.full_name)
    entity = await repo.save(entity)

    if body.file_ids:
        await repo.add_images(entity.id, body.file_ids)

    await repo.db.refresh(entity)

    return entity_to_response(entity)
