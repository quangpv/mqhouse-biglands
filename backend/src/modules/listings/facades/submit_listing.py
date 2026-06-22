import uuid

from fastapi import Depends

from src.data.entities.listing import ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.listing_image_repo import ListingImageRepo
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.notifications.service import NotificationService
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import ListingResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import BadRequestError, ForbiddenError, NotFoundError
from src.shared.utils.notification_formatter import format_notification_title
from src.shared.utils.status_machine import validate_transition


async def submit_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    image_repo: ListingImageRepo = Depends(ListingImageRepo),
    user_repo: UserRepo = Depends(UserRepo),
    notification_service: NotificationService = Depends(NotificationService),
) -> ListingResponse:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise ForbiddenError("Only the listing owner can submit")

    validate_transition(listing.status, ListingStatus.PENDING_APPROVAL)

    image_count = await image_repo.count_by_listing(listing_id)
    if image_count == 0:
        raise BadRequestError("At least one image is required before submitting")

    listing.status = ListingStatus.PENDING_APPROVAL
    listing.approval_version += 1
    listing = await repo.save(listing)

    approvers = await user_repo.list_by_roles(UserRole.APPROVER, UserRole.ADMIN)
    for approver in approvers:
        await notification_service.send(
            user_id=approver.id, event_type="listing_post_created",
            title=format_notification_title(
                event_type="listing_post_created",
                transaction_type=listing.transaction_type.value,
                actor_name=current_user.full_name,
                item_code=listing.code,
            ),
            body=f"Listing {listing.title} has been submitted by {current_user.full_name}.",
            reference_type=ReferenceType.LISTING, reference_id=listing_id,
            actor_name=current_user.full_name,
            transaction_type=listing.transaction_type.value,
        )

    return listing_to_response(listing)
