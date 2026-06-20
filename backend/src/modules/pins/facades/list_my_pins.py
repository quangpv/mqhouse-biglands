from math import ceil

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.user_pin_repo import UserPinRepo
from src.modules.pins.mapper import pinned_listing_to_response
from src.modules.pins.schemas import PinnedListingListResponse
from src.platform.auth import get_current_user


async def list_my_pins(
    page: int = 1,
    per_page: int = 20,
    current_user: UserEntity = Depends(get_current_user),
    pin_repo: UserPinRepo = Depends(UserPinRepo),
) -> PinnedListingListResponse:
    total = await pin_repo.count_by_user(current_user.id)
    listings = await pin_repo.get_pinned_listings_paginated(current_user.id, page, per_page)

    return PinnedListingListResponse(
        data=[pinned_listing_to_response(listing) for listing in listings],
        total=total,
        page=page,
        size=per_page,
        total_pages=ceil(total / per_page) if per_page > 0 else 0,
    )
