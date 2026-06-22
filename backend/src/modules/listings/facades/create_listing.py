from fastapi import Depends

from src.data.entities.listing import ListingEntity, ListingStatus
from src.data.entities.notification import ReferenceType
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.listing_repo import ListingRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.listings.mapper import listing_to_response
from src.modules.listings.schemas import CreateListingRequest, ListingResponse
from src.modules.notifications.service import NotificationService
from src.platform.auth import get_current_user
from src.shared.utils.code_generator import generate_product_code
from src.shared.utils.notification_formatter import format_notification_title


async def create_listing(
    data: CreateListingRequest,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
    user_repo: UserRepo = Depends(UserRepo),
    notification_service: NotificationService = Depends(NotificationService),
) -> ListingResponse:
    listing = ListingEntity(
        code=generate_product_code(),
        transaction_type=data.transaction_type,
        property_type=data.property_type,
        title=data.title,
        description=data.description,
        price=data.price,
        commission_type=data.commission_type,
        commission_value=data.commission_value,
        area_width=data.area_width,
        area_length=data.area_length,
        total_area=data.total_area,
        num_rooms=data.num_rooms,
        num_bathrooms=data.num_bathrooms,
        num_floors=data.num_floors,
        street_name=data.street_name,
        house_number=data.house_number,
        address=data.address,
        ward=data.ward,
        district=data.district,
        city=data.city,
        latitude=data.latitude,
        longitude=data.longitude,
        label=data.label,
        furnishing=data.furnishing,
        frontage_type=data.frontage_type,
        legal_status=data.legal_status,
        direction=data.direction,
        road_width=data.road_width,
        owner_phone=data.owner_phone,
        video_url=data.video_url,
        created_by_id=current_user.id,
        status=ListingStatus.DRAFT,
    )

    if data.action == "submit":
        listing.status = ListingStatus.PENDING_APPROVAL

    if current_user.role == UserRole.ADMIN:
        listing.status = ListingStatus.CON_HANG
        listing.approved_by_id = current_user.id
        listing.approved_at = listing.created_at

        listing.approval_version = 1
        listing = await repo.create(listing)

    if data.action == "submit" and current_user.role != UserRole.ADMIN:
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
                reference_type=ReferenceType.LISTING, reference_id=listing.id,
                actor_name=current_user.full_name,
                transaction_type=listing.transaction_type.value,
            )

    return listing_to_response(listing)
