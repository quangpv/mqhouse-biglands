import uuid

from fastapi import Depends, Path, Query

from src.data.entities.user import UserEntity
from src.data.repositories.property_repo import PropertyRepo
from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import entity_to_response
from src.modules.reviews.schemas import PageDTO, ReviewListResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def list_reviews(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    repo: ReviewRepo = Depends(ReviewRepo),
    prop_repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ReviewListResponse:
    prop = await prop_repo.get(property_id)
    if prop is None:
        raise NotFoundError("Property not found")

    rows, total = await repo.list_by_property(property_id, page=page, size=size)
    total_pages = (total + size - 1) // size if total > 0 else 0

    return ReviewListResponse(
        data=[entity_to_response(r) for r in rows],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
