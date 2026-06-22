from datetime import datetime, timezone

from src.data.entities.approval import ApprovalEntity, ApprovalType, DecisionType
from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingEntity, ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo

APPROVAL_TYPE_MAP = {
    DealEventType.DEPOSIT_REPORTED: ApprovalType.DEPOSIT,
    DealEventType.CLOSURE_REPORTED: ApprovalType.CLOSURE,
    DealEventType.CANCELLATION_REPORTED: ApprovalType.CANCELLATION,
    DealEventType.SOLD_OUT_REPORTED: ApprovalType.SOLD_OUT,
}

CONFIRMED_EVENT_MAP = {
    ApprovalType.DEPOSIT: DealEventType.DEPOSIT_CONFIRMED,
    ApprovalType.CLOSURE: DealEventType.CLOSURE_CONFIRMED,
    ApprovalType.CANCELLATION: DealEventType.CANCELLATION_CONFIRMED,
    ApprovalType.SOLD_OUT: DealEventType.SOLD_OUT_CONFIRMED,
}

APPROVED_STATUS_MAP = {
    ApprovalType.DEPOSIT: ListingStatus.DA_COC,
    ApprovalType.CLOSURE: ListingStatus.DA_CHOT,
    ApprovalType.CANCELLATION: ListingStatus.CON_HANG,
    ApprovalType.SOLD_OUT: ListingStatus.HET_HANG,
}


async def auto_approve_deal_event(
    listing: ListingEntity,
    reported_event: DealEventEntity,
    current_user: UserEntity,
    deal_repo: DealEventRepo,
    listing_repo: ListingRepo,
    approval_repo: ApprovalRepo,
) -> None:
    approval_type = APPROVAL_TYPE_MAP[reported_event.event_type]
    new_status = APPROVED_STATUS_MAP[approval_type]
    now = datetime.now(timezone.utc)

    reported_event.confirmed_by_id = current_user.id
    reported_event.confirmed_at = now
    await deal_repo.save(reported_event)

    confirmed = DealEventEntity(
        listing_id=listing.id,
        event_type=CONFIRMED_EVENT_MAP[approval_type],
        reported_by_id=reported_event.reported_by_id,
        confirmed_by_id=current_user.id,
        confirmed_at=now,
        notes=reported_event.notes,
        customer_name=reported_event.customer_name,
        customer_phone=reported_event.customer_phone,
        deposit_amount=reported_event.deposit_amount,
    )
    await deal_repo.create(confirmed)

    listing.status = new_status
    await listing_repo.save(listing)

    approval = ApprovalEntity(
        listing_id=listing.id,
        approval_type=approval_type,
        decision=DecisionType.APPROVED,
        decided_by_id=current_user.id,
        version=1,
    )
    await approval_repo.create(approval)
