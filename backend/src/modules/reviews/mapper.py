from src.data.entities.review import ReviewEntity
from src.data.entities.review_image import ReviewImageEntity
from src.modules.reviews.schemas import ReviewImageResponse, ReviewResponse


def review_image_to_response(entity: ReviewImageEntity) -> ReviewImageResponse:
    return ReviewImageResponse(
        id=entity.id,
        url=entity.url,
        order=entity.order,
    )


def review_to_response(entity: ReviewEntity) -> ReviewResponse:
    return ReviewResponse(
        id=entity.id,
        listing_id=entity.listing_id,
        author_id=entity.author_id,
        author_name=entity.author_name,
        content=entity.content,
        images=[review_image_to_response(img) for img in (entity.images or [])],
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
