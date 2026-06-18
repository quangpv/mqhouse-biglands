from src.data.entities.listing import ListingEntity
from src.modules.hot_products.schemas import HotListingResponse


def listing_to_hot_response(entity: ListingEntity) -> HotListingResponse:
    return HotListingResponse(
        id=entity.id,
        code=entity.code,
        transaction_type=entity.transaction_type.value,
        property_type=entity.property_type.value,
        title=entity.title,
        price=entity.price,
        status=entity.status.value,
        hot_order=entity.hot_order,
        view_count=entity.view_count,
        created_by_id=entity.created_by_id,
        created_at=entity.created_at,
    )
