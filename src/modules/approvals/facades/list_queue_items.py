from math import ceil

from fastapi import Depends

from src.data.entities.approval import ApprovalType
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.mapper import deal_event_to_queue_item, listing_to_queue_item
from src.modules.approvals.schemas import QueueItemListResponse
from src.shared.errors.exceptions import BadRequestError
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
        raise BadRequestError(f"Invalid queue type: {queue_type}")

    if approval_type == ApprovalType.LISTING_POST:
        items: list = await repo.list_listing_post_queue_items(transaction_type)
        mapped = [listing_to_queue_item(item) for item in items]
    else:
        raw = await repo.list_deal_event_queue_items(approval_type, transaction_type)
        mapped = [deal_event_to_queue_item(listing, event, approval_type) for listing, event in raw]

    total = len(mapped)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = mapped[start:end]

    return QueueItemListResponse(
        data=page_items,
        total=total,
        page=page,
        size=per_page,
        total_pages=ceil(total / per_page) if per_page > 0 else 0,
    )
