from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_pin_repo import UserPinRepo
from src.modules.listings.schemas import FilterCounts
from src.platform.auth import get_current_user


async def get_filter_counts(
    current_user: UserEntity | None = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    pin_repo: UserPinRepo = Depends(UserPinRepo),
) -> FilterCounts:
    total_count = await repo.count_active()
    hot_count = await repo.count_hot_listings()
    pinned_count = await pin_repo.count_active_pins_by_user(current_user.id) if current_user else 0
    return FilterCounts(all=total_count, hot=hot_count, pinned=pinned_count)
