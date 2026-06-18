from math import ceil

from fastapi import Depends, HTTPException, status

from src.data.entities.approval import ApprovalType
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.mapper import queue_item_to_response
from src.modules.approvals.schemas import QueueItemListResponse
from src.shared.pagination import PaginationParams


async def list_queue_items(
    queue_type: str,
    transaction_type: str | None = None,
    page: int = 1,
    per_page: int = 20,
    repo: ApprovalRepo = Depends(ApprovalRepo),
) -> QueueItemListResponse:
    try:
        approval_type = ApprovalType(queue_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid queue type: {queue_type}")

    if approval_type == ApprovalType.LISTING_POST:
        items = await repo.list_listing_post_queue_items(transaction_type)
    else:
        items = await repo.list_deal_event_queue_items(approval_type, transaction_type)

    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]

    return QueueItemListResponse(
        data=[queue_item_to_response(item) for item in page_items],
        total=total,
        page=page,
        size=per_page,
        total_pages=ceil(total / per_page) if per_page > 0 else 0,
    )
