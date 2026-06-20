from datetime import datetime, timezone

from fastapi import Depends

from src.data.entities.approval import ApprovalEntity, ApprovalType, DecisionType
from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.approvals.schemas import BulkApproveItem, BulkApproveRequest, BulkApproveResponse
from src.platform.auth import get_current_user


async def bulk_approve(
    data: BulkApproveRequest,
    current_user: UserEntity = Depends(get_current_user),
    listing_repo: ListingRepo = Depends(ListingRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
) -> BulkApproveResponse:
    results: list[BulkApproveItem] = []
    succeeded = 0
    failed = 0

    for listing_id in data.listing_ids:
        listing = await listing_repo.get(listing_id)
        if listing is None:
            results.append(BulkApproveItem(listing_id=listing_id, success=False, message="Listing not found"))
            failed += 1
            continue

        if listing.status != ListingStatus.PENDING_APPROVAL:
            results.append(BulkApproveItem(listing_id=listing_id, success=False, message="Listing is not pending approval"))
            failed += 1
            continue

        existing = await approval_repo.get_approval_by_listing_and_type(listing_id, ApprovalType.LISTING_POST)
        if existing is not None:
            results.append(BulkApproveItem(listing_id=listing_id, success=False, message=f"Already processed: {existing.decision.value}"))
            failed += 1
            continue

        listing.status = ListingStatus.CON_HANG
        listing.approved_by_id = current_user.id
        listing.approved_at = datetime.now(timezone.utc)
        await listing_repo.save(listing)

        approval = ApprovalEntity(
            listing_id=listing_id,
            approval_type=ApprovalType.LISTING_POST,
            decision=DecisionType.APPROVED,
            decided_by_id=current_user.id,
        )
        await approval_repo.create(approval)

        results.append(BulkApproveItem(listing_id=listing_id, success=True, message="Approved"))
        succeeded += 1

    return BulkApproveResponse(
        results=results,
        total=len(data.listing_ids),
        succeeded=succeeded,
        failed=failed,
    )
