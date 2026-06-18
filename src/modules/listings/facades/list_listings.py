from fastapi import Depends, Query

from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingListResponse, ListingResponse
from src.platform.auth import get_current_user
from src.platform.dependencies import get_db
from src.shared.pagination import build_paginated_response, paginate


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
    db=Depends(get_db),
    repo: ListingRepo = Depends(ListingRepo),
) -> ListingListResponse:
    resolved_owner_id = current_user.id if owner_id == "me" else (None if owner_id is None else owner_id)
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
    rows, total = await paginate(db, query, page=page, size=size)
    items = [listing_to_response(l) for l in rows]
    total_count = await repo.count_active()
    return ListingListResponse(
        **build_paginated_response(items, page, size, total).model_dump(),
        total_count=total_count,
    )
