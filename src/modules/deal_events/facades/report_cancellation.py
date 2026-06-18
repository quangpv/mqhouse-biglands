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
from src.modules.deal_events.schemas import DealEventResponse, ReportCancellationRequest
from src.platform.auth import get_current_user
from src.platform.dependencies import get_db
from src.shared.errors.exceptions import NotFoundError


async def report_cancellation(
    listing_id: uuid.UUID,
    data: ReportCancellationRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    user_repo: UserRepo = Depends(UserRepo),
    db: AsyncSession = Depends(get_db),
) -> DealEventResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.DA_COC:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Listing must be in DA_COC to report a cancellation")

    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.CANCELLATION_REPORTED,
        reported_by_id=current_user.id,
        notes=data.notes,
    )
    event = await deal_repo.create(event)

    approvers = await user_repo.list_by_role(UserRole.APPROVER)
    for approver in approvers:
        await send_notification(
            db=db, user_id=approver.id, event_type="cancellation_reported",
            title=f"Cancellation reported for listing {listing.code}",
            body=f"A cancellation has been reported by {current_user.full_name}.",
            reference_type=ReferenceType.DEAL_EVENT, reference_id=event.id,
        )

    return deal_event_to_response(event)
