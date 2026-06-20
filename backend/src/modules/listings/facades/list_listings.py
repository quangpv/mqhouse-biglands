import uuid

from fastapi import Depends, Query

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingListResponse
from src.platform.auth import get_current_user
from src.shared.pagination import build_paginated_response


async def list_listings(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    transaction_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    property_type: str | None = Query(default=None),
    filter_by: str | None = Query(default=None),
    sort_by: str | None = Query(default=None),
    sort_order: str | None = Query(default=None),
    owner_id: str | None = Query(default=None, description="Filter by owner. Use 'me' for current user."),
    current_user: UserEntity | None = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
) -> ListingListResponse:
    resolved_owner_id: uuid.UUID | None = None
    if owner_id == "me":
        if current_user is not None:
            resolved_owner_id = current_user.id
    elif owner_id is not None:
        resolved_owner_id = uuid.UUID(owner_id)
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
    )
    rows, total = await repo.paginated_list(query, page=page, size=size)
    items = [listing_to_response(listing) for listing in rows]
    total_count = await repo.count_active()
    return ListingListResponse(
        **build_paginated_response(items, page, size, total).model_dump(),
        total_count=total_count,
    )
