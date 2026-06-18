from src.data.entities.listing import ListingEntity
from src.modules.pins.schemas import PinnedListingResponse


def pinned_listing_to_response(entity: ListingEntity) -> PinnedListingResponse:
    return PinnedListingResponse(
        id=entity.id,
        code=entity.code,
        transaction_type=entity.transaction_type.value,
        property_type=entity.property_type.value,
        title=entity.title,
        description=entity.description,
        price=entity.price,
        status=entity.status.value,
        is_hot=entity.is_hot,
        view_count=entity.view_count,
        created_by_id=entity.created_by_id,
        created_at=entity.created_at,
        is_pinned=True,
    )
