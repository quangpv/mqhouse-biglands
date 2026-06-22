import uuid

from fastapi import Depends, Query

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_pin_repo import UserPinRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import FilterCounts, ListingListResponse
from src.platform.auth import get_current_user
from src.shared.pagination import build_paginated_response


async def list_listings(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    transaction_type: str | None = Query(default=None),
    status: list[str] | None = Query(default=None),
    property_type: str | None = Query(default=None),
    filter_by: str | None = Query(default=None),
    sort_by: str | None = Query(default=None),
    sort_order: str | None = Query(default=None),
    owner_id: str | None = Query(default=None, description="Filter by owner. Use 'me' for current user."),
    created_by: str | None = Query(default=None, alias="createdBy", description="Filter by creator. Use 'me' for current user."),
    is_hot: bool | None = Query(default=None, alias="isHot"),
    current_user: UserEntity | None = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    pin_repo: UserPinRepo = Depends(UserPinRepo),
) -> ListingListResponse:
    resolved_owner_id: uuid.UUID | None = None
    owner_source = created_by or owner_id
    if owner_source == "me":
        if current_user is not None:
            resolved_owner_id = current_user.id
    elif owner_source is not None:
        resolved_owner_id = uuid.UUID(owner_source)
    if resolved_owner_id is None and current_user is not None and current_user.role != UserRole.ADMIN:
        resolved_owner_id = current_user.id
    query = repo.build_list_query(
        search=search,
        transaction_type=transaction_type,
        status=status,
        property_type=property_type,
        filter_by=filter_by,
        sort_by=sort_by,
        sort_order=sort_order,
        owner_id=resolved_owner_id,
        is_hot=is_hot,
    )
    rows, total = await repo.paginated_list(query, page=page, size=size)
    items = [listing_to_response(listing, current_user=current_user) for listing in rows]
    total_count = await repo.count_active()
    hot_count = await repo.count_hot_listings()
    pinned_count = await pin_repo.count_by_user(current_user.id) if current_user else 0
    filter_counts = FilterCounts(all=total_count, hot=hot_count, pinned=pinned_count)
    return ListingListResponse(
        **build_paginated_response(items, page, size, total).model_dump(),
        total_count=total_count,
        filter_counts=filter_counts,
    )
