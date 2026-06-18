from src.data.entities.listing_image import ListingImageEntity
from src.modules.listing_images.schemas import ImageResponse


def image_to_response(entity: ListingImageEntity) -> ImageResponse:
    return ImageResponse(
        id=entity.id,
        listing_id=entity.listing_id,
        url=entity.url,
        order=entity.order,
        is_primary=entity.is_primary,
    )
