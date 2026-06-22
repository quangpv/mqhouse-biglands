import uuid

from fastapi import Depends

from src.data.entities.approval import ApprovalEntity, ApprovalType, DecisionType
from src.data.entities.deal_event import DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.approvals.mapper import approval_to_response
from src.modules.notifications.service import NotificationService
from src.modules.approvals.schemas import ApproveResponse, RejectRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError
from src.shared.utils.notification_formatter import format_notification_title

REJECTED_STATUS_MAP = {
    ApprovalType.LISTING_POST: ListingStatus.DRAFT,
    ApprovalType.DEPOSIT: ListingStatus.CON_HANG,
    ApprovalType.CLOSURE: ListingStatus.DA_COC,
    ApprovalType.CANCELLATION: ListingStatus.DA_COC,
    ApprovalType.SOLD_OUT: ListingStatus.CON_HANG,
}


async def reject_item(
    listing_id: uuid.UUID,
    data: RejectRequest,
    current_user: UserEntity = Depends(get_current_user),
    listing_repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    notification_service: NotificationService = Depends(NotificationService),
) -> ApproveResponse:
    listing = await listing_repo.get_with_lock(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id == current_user.id and current_user.role != UserRole.ADMIN:
        raise ConflictError("Approver cannot reject their own listing")

    approval_type = None
    deal_event = None

    if listing.status == ListingStatus.PENDING_APPROVAL:
        approval_type = ApprovalType.LISTING_POST
    elif listing.status == ListingStatus.CON_HANG:
        deal_event = await deal_repo.get_pending_confirmation(listing_id, DealEventType.DEPOSIT_REPORTED)
        if deal_event:
            approval_type = ApprovalType.DEPOSIT
        else:
            deal_event = await deal_repo.get_pending_confirmation(listing_id, DealEventType.SOLD_OUT_REPORTED)
            if deal_event:
                approval_type = ApprovalType.SOLD_OUT
    elif listing.status == ListingStatus.DA_COC:
        deal_event = await deal_repo.get_pending_confirmation(listing_id, DealEventType.CLOSURE_REPORTED)
        if deal_event:
            approval_type = ApprovalType.CLOSURE
        else:
            deal_event = await deal_repo.get_pending_confirmation(listing_id, DealEventType.CANCELLATION_REPORTED)
            if deal_event:
                approval_type = ApprovalType.CANCELLATION

    if approval_type is None:
        raise ConflictError(detail="No pending approval request found for this listing")

    if approval_type == ApprovalType.LISTING_POST:
        existing = await approval_repo.get_by_listing_type_and_version(listing_id, approval_type, listing.approval_version)
    else:
        existing = await approval_repo.get_approval_by_listing_and_type(listing_id, approval_type)
    if existing is not None:
        raise ConflictError(detail=f"Approval already processed: {existing.decision.value}")

    new_status = REJECTED_STATUS_MAP[approval_type]

    listing.status = new_status
    await listing_repo.save(listing)

    if deal_event is not None:
        deal_event.notes = data.reason
        await deal_repo.save(deal_event)

    approval = ApprovalEntity(
        listing_id=listing_id,
        approval_type=approval_type,
        decision=DecisionType.REJECTED,
        decided_by_id=current_user.id,
        reason=data.reason,
        version=listing.approval_version if approval_type == ApprovalType.LISTING_POST else 1,
    )
    approval = await approval_repo.create(approval)

    event_type_key = {
        ApprovalType.LISTING_POST: "listing_post_rejected",
        ApprovalType.DEPOSIT: "deposit_rejected",
        ApprovalType.CLOSURE: "closure_rejected",
        ApprovalType.CANCELLATION: "cancellation_rejected",
        ApprovalType.SOLD_OUT: "sold_out_rejected",
    }[approval_type]
    if listing.created_by_id != current_user.id:
        await notification_service.send(
            user_id=listing.created_by_id, event_type=event_type_key,
            title=format_notification_title(
                event_type=event_type_key,
                transaction_type=listing.transaction_type.value,
                actor_name=current_user.full_name,
                item_code=listing.code,
            ),
            body=f"Your listing {listing.title} was rejected. Reason: {data.reason}",
            reference_type=ReferenceType.LISTING, reference_id=listing_id,
            actor_name=current_user.full_name,
            transaction_type=listing.transaction_type.value,
        )

    return approval_to_response({
        "id": approval.id,
        "listing_id": listing_id,
        "listing_code": listing.code,
        "approval_type": approval_type,
        "decision": DecisionType.REJECTED,
        "listing_status": new_status,
        "created_at": approval.created_at,
    })
