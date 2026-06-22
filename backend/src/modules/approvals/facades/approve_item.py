import uuid
from datetime import datetime, timezone

from fastapi import Depends

from src.data.entities.approval import ApprovalEntity, ApprovalType, DecisionType
from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.approvals.mapper import approval_to_response
from src.modules.notifications.service import NotificationService
from src.modules.approvals.schemas import ApproveResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError
from src.shared.utils.notification_formatter import format_notification_title

APPROVED_STATUS_MAP = {
    ApprovalType.LISTING_POST: ListingStatus.CON_HANG,
    ApprovalType.DEPOSIT: ListingStatus.DA_COC,
    ApprovalType.CLOSURE: ListingStatus.DA_CHOT,
    ApprovalType.CANCELLATION: ListingStatus.CON_HANG,
    ApprovalType.SOLD_OUT: ListingStatus.HET_HANG,
}

APPROVAL_TO_CONFIRMED_EVENT = {
    ApprovalType.DEPOSIT: DealEventType.DEPOSIT_CONFIRMED,
    ApprovalType.CLOSURE: DealEventType.CLOSURE_CONFIRMED,
    ApprovalType.CANCELLATION: DealEventType.CANCELLATION_CONFIRMED,
    ApprovalType.SOLD_OUT: DealEventType.SOLD_OUT_CONFIRMED,
}


async def approve_item(
    listing_id: uuid.UUID,
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
        raise ConflictError("Approver cannot approve their own listing")

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

    new_status = APPROVED_STATUS_MAP[approval_type]
    now = datetime.now(timezone.utc)

    listing.status = new_status
    if new_status == ListingStatus.CON_HANG:
        listing.approved_by_id = current_user.id
        listing.approved_at = now
    await listing_repo.save(listing)

    if deal_event is not None:
        confirmed_event = DealEventEntity(
            listing_id=listing_id,
            event_type=APPROVAL_TO_CONFIRMED_EVENT[approval_type],
            reported_by_id=deal_event.reported_by_id,
            confirmed_by_id=current_user.id,
            confirmed_at=now,
            notes=deal_event.notes,
            customer_name=deal_event.customer_name,
            customer_phone=deal_event.customer_phone,
            deposit_amount=deal_event.deposit_amount,
        )
        await deal_repo.create(confirmed_event)

    approval = ApprovalEntity(
        listing_id=listing_id,
        approval_type=approval_type,
        decision=DecisionType.APPROVED,
        decided_by_id=current_user.id,
        version=listing.approval_version if approval_type == ApprovalType.LISTING_POST else 1,
    )
    approval = await approval_repo.create(approval)

    event_type_key = {
        ApprovalType.LISTING_POST: "listing_post_approved",
        ApprovalType.DEPOSIT: "deposit_confirmed",
        ApprovalType.CLOSURE: "closure_confirmed",
        ApprovalType.CANCELLATION: "cancellation_confirmed",
        ApprovalType.SOLD_OUT: "sold_out_confirmed",
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
            body=f"Your listing {listing.title} has been approved by {current_user.full_name}.",
            reference_type=ReferenceType.LISTING, reference_id=listing_id,
            actor_name=current_user.full_name,
            transaction_type=listing.transaction_type.value,
        )

    return approval_to_response({
        "id": approval.id,
        "listing_id": listing_id,
        "listing_code": listing.code,
        "approval_type": approval_type,
        "decision": DecisionType.APPROVED,
        "listing_status": new_status,
        "created_at": approval.created_at,
    })
