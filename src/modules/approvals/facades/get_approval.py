import uuid

from fastapi import Depends, HTTPException, status

from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.mapper import queue_item_to_response
from src.modules.approvals.schemas import ApprovalDetailResponse


async def get_approval(
    listing_id: uuid.UUID,
    repo: ApprovalRepo = Depends(ApprovalRepo),
) -> ApprovalDetailResponse:
    item = await repo.get_pending_listing_post(listing_id)
    if item is None:
        item = await repo.get_pending_deal_event_by_listing(listing_id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending approval found for this listing")

    existing = await repo.get_approval_by_listing_and_type(listing_id, item["approval_type"])

    return ApprovalDetailResponse(
        id=item["id"],
        listing_id=item["listing_id"],
        listing_code=item["listing_code"],
        approval_type=item["approval_type"].value,
        transaction_type=item["transaction_type"].value,
        title=item.get("title"),
        price=item.get("price"),
        listing_status=item["status"].value if hasattr(item["status"], "value") else str(item["status"]),
        created_at=item["created_at"],
        customer_name=item.get("customer_name"),
        customer_phone=item.get("customer_phone"),
        deposit_amount=item.get("deposit_amount"),
        event_notes=item.get("event_notes"),
        has_existing_approval=existing is not None,
        existing_decision=existing.decision.value if existing else None,
    )
