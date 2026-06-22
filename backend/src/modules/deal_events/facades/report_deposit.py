import uuid

from fastapi import Depends

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.approvals.services.approval_service import auto_approve_deal_event
from src.modules.deal_events.mapper import deal_event_to_response
from src.modules.notifications.service import NotificationService
from src.modules.deal_events.schemas import DealEventResponse, ReportDepositRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError
from src.shared.utils.notification_formatter import format_notification_title


async def report_deposit(
    listing_id: uuid.UUID,
    data: ReportDepositRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    user_repo: UserRepo = Depends(UserRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    notification_service: NotificationService = Depends(NotificationService),
) -> DealEventResponse:
    listing = await repo.get_with_lock(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.CON_HANG:
        raise ConflictError("Listing must be in CON_HANG to report a deposit")
    if await deal_repo.has_active_deposit(listing_id):
        raise ConflictError("An active deposit already exists for this listing")

    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.DEPOSIT_REPORTED,
        reported_by_id=current_user.id,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        deposit_amount=data.deposit_amount,
        notes=data.notes,
    )
    event = await deal_repo.create(event)

    if current_user.role == UserRole.ADMIN:
        await auto_approve_deal_event(listing, event, current_user, deal_repo, repo, approval_repo)
        if listing.created_by_id != current_user.id:
            await notification_service.send(
                user_id=listing.created_by_id, event_type="deposit_confirmed",
                title=format_notification_title(
                    event_type="deposit_confirmed",
                    transaction_type=listing.transaction_type.value,
                    actor_name=current_user.full_name,
                    item_code=listing.code,
                ),
                body=f"A deposit of {data.deposit_amount} has been confirmed by admin {current_user.full_name}.",
                reference_type=ReferenceType.LISTING, reference_id=listing_id,
                actor_name=current_user.full_name,
                transaction_type=listing.transaction_type.value,
            )
    else:
        approvers = await user_repo.list_by_roles(UserRole.APPROVER, UserRole.ADMIN)
        for approver in approvers:
            await notification_service.send(
                user_id=approver.id, event_type="deposit_reported",
                title=format_notification_title(
                    event_type="deposit_reported",
                    transaction_type=listing.transaction_type.value,
                    actor_name=current_user.full_name,
                    item_code=listing.code,
                ),
                body=f"A deposit of {data.deposit_amount} has been reported by {current_user.full_name}.",
                reference_type=ReferenceType.DEAL_EVENT, reference_id=event.id,
                actor_name=current_user.full_name,
                transaction_type=listing.transaction_type.value,
            )

    return deal_event_to_response(event)
