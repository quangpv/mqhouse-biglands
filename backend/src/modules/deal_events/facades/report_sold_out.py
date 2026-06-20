import uuid

from fastapi import Depends

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.notification_repo import NotificationRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.deal_events.mapper import deal_event_to_response
from src.modules.deal_events.schemas import DealEventResponse, ReportSoldOutRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def report_sold_out(
    listing_id: uuid.UUID,
    data: ReportSoldOutRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
    user_repo: UserRepo = Depends(UserRepo),
    notification_repo: NotificationRepo = Depends(NotificationRepo),
) -> DealEventResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.CON_HANG:
        raise ConflictError("Listing must be in CON_HANG to report sold out")

    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.SOLD_OUT_REPORTED,
        reported_by_id=current_user.id,
        notes=data.notes,
    )
    event = await deal_repo.create(event)

    approvers = await user_repo.list_by_role(UserRole.APPROVER)
    for approver in approvers:
        await notification_repo.send(
            user_id=approver.id, event_type="sold_out_reported",
            title=f"Sold out reported for listing {listing.code}",
            body=f"Sold out has been reported by {current_user.full_name}.",
            reference_type=ReferenceType.DEAL_EVENT, reference_id=event.id,
        )

    return deal_event_to_response(event)
