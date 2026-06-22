import uuid

from fastapi import Depends

from src.data.repositories.review_repo import ReviewRepo
from src.modules.reviews.mapper import review_to_response
from src.modules.reviews.schemas import ReviewListResponse
from src.shared.pagination import build_paginated_response


async def list_reviews(
    listing_id: uuid.UUID,
    page: int = 1,
    size: int = 20,
    repo: ReviewRepo = Depends(ReviewRepo),
) -> ReviewListResponse:
    reviews, total = await repo.list_by_listing(listing_id, page=page, size=size)
    items = [review_to_response(r) for r in reviews]
    return ReviewListResponse(
        **build_paginated_response(items, page, size, total).model_dump(),
    )
