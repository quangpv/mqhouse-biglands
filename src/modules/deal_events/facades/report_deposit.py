import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.notifications import send_notification
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.deal_events.mapper import deal_event_to_response
from src.modules.deal_events.schemas import DealEventResponse, ReportDepositRequest
from src.platform.auth import get_current_user
from src.platform.dependencies import get_db
from src.shared.errors.exceptions import NotFoundError


async def report_deposit(
    listing_id: uuid.UUID,
    data: ReportDepositRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    user_repo: UserRepo = Depends(UserRepo),
    db: AsyncSession = Depends(get_db),
) -> DealEventResponse:
    listing = await repo.get_with_lock(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.CON_HANG:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Listing must be in CON_HANG to report a deposit")
    if await deal_repo.has_active_deposit(listing_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An active deposit already exists for this listing")

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

    approvers = await user_repo.list_by_role(UserRole.APPROVER)
    for approver in approvers:
        await send_notification(
            db=db, user_id=approver.id, event_type="deposit_reported",
            title=f"Deposit reported for listing {listing.code}",
            body=f"A deposit of {data.deposit_amount} has been reported by {current_user.full_name}.",
            reference_type=ReferenceType.DEAL_EVENT, reference_id=event.id,
        )

    return deal_event_to_response(event)
