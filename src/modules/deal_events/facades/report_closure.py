import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.deal_event_repo import DealEventRepo
from src.data.repositories.listing_repo import ListingRepo
from src.modules.deal_events.mapper import deal_event_to_response
from src.modules.deal_events.schemas import DealEventResponse, ReportClosureRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def report_closure(
    listing_id: uuid.UUID,
    data: ReportClosureRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    deal_repo: DealEventRepo = Depends(DealEventRepo),
) -> DealEventResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")
    if listing.status != ListingStatus.DA_COC:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Listing must be in DA_COC to report a closure")

    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.CLOSURE_REPORTED,
        reported_by_id=current_user.id,
        notes=data.notes,
    )
    event = await deal_repo.create(event)
    return deal_event_to_response(event)
