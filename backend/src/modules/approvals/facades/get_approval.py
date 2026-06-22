import uuid

from fastapi import Depends

from src.data.entities.approval import ApprovalType
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.schemas import ApprovalDetailResponse
from src.shared.errors.exceptions import NotFoundError


async def get_approval(
    listing_id: uuid.UUID,
    repo: ApprovalRepo = Depends(ApprovalRepo),
) -> ApprovalDetailResponse:
    listing = await repo.get_pending_listing_post(listing_id)
    if listing is not None:
        existing = await repo.get_by_listing_type_and_version(listing_id, ApprovalType.LISTING_POST, listing.approval_version)
        return ApprovalDetailResponse(
            id=listing.id,
            listing_id=listing.id,
            listing_code=listing.code,
            approval_type=ApprovalType.LISTING_POST.value,
            transaction_type=listing.transaction_type.value,
            title=listing.title,
            price=listing.price,
            listing_status=listing.status.value,
            created_at=listing.created_at,
            has_existing_approval=existing is not None,
            existing_decision=existing.decision.value if existing else None,
        )

    result = await repo.get_pending_deal_event_by_listing(listing_id)
    if result is None:
        raise NotFoundError("No pending approval found for this listing")

    listing, event, approval_type = result
    existing = await repo.get_approval_by_listing_and_type(listing_id, approval_type)

    return ApprovalDetailResponse(
        id=listing.id,
        listing_id=listing.id,
        listing_code=listing.code,
        approval_type=approval_type.value,
        transaction_type=listing.transaction_type.value,
        title=listing.title,
        price=listing.price,
        listing_status=listing.status.value,
        created_at=event.created_at,
        customer_name=event.customer_name,
        customer_phone=event.customer_phone,
        deposit_amount=event.deposit_amount,
        event_notes=event.notes,
        has_existing_approval=existing is not None,
        existing_decision=existing.decision.value if existing else None,
    )
