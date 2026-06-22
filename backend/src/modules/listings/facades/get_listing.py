import uuid

from fastapi import Depends

from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.user_pin_repo import UserPinRepo
from src.data.entities.user import UserEntity
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingDetailResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def get_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity | None = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    pin_repo: UserPinRepo = Depends(UserPinRepo),
) -> ListingDetailResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    listing.view_count = (listing.view_count or 0) + 1
    await repo.save(listing)

    base = listing_to_response(listing, current_user=current_user)
    images = await image_repo.list_by_listing(listing_id)
    deal_events = await deal_repo.get_by_listing(listing_id)
    is_pinned = await pin_repo.get_by_user_and_listing(current_user.id, listing_id) is not None if current_user else False

    return ListingDetailResponse(
        **base.model_dump(),
        images=[{"id": img.id, "url": img.url, "order": img.order, "is_primary": img.is_primary} for img in images],
        deal_events=[{"id": e.id, "event_type": e.event_type.value, "created_at": e.created_at} for e in deal_events],
        is_pinned=is_pinned,
    )
