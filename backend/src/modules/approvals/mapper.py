from src.data.entities.approval import ApprovalType
from src.data.entities.deal_event import DealEventEntity
from src.data.entities.listing import ListingEntity
from src.data.entities.user import UserEntity
from src.modules.approvals.schemas import ApproveResponse, DealEventInfo, QueueItemResponse, ReporterInfo


def _map_listing_fields(listing: ListingEntity) -> dict:
    primary_image = next(
        (img for img in (listing.images or []) if img.is_primary), None
    )
    price_per_m2 = listing.price / listing.total_area if listing.total_area > 0 else None
    return {
        "total_area": listing.total_area,
        "price_per_m2": price_per_m2,
        "area_width": listing.area_width,
        "area_length": listing.area_length,
        "num_rooms": listing.num_rooms,
        "num_bathrooms": listing.num_bathrooms,
        "num_floors": listing.num_floors,
        "street_name": listing.street_name,
        "ward": listing.ward,
        "district": listing.district,
        "city": listing.city,
        "address": listing.address,
        "is_hot": bool(listing.is_hot) if listing.is_hot else False,
        "is_pinned": False,
        "hot_order": listing.hot_order,
        "primary_image_url": primary_image.url if primary_image else None,
        "created_by_id": listing.created_by_id,
        "creator_name": listing.created_by.full_name if listing.created_by else None,
        "listing_created_at": listing.created_at,
    }


def listing_to_queue_item(listing: ListingEntity) -> QueueItemResponse:
    return QueueItemResponse(
        id=listing.id,
        listing_id=listing.id,
        listing_code=listing.code,
        approval_type=ApprovalType.LISTING_POST.value,
        transaction_type=listing.transaction_type.value,
        title=listing.title,
        price=listing.price,
        status=listing.status.value,
        created_at=listing.created_at,
        **_map_listing_fields(listing),
    )


def deal_event_to_queue_item(
    listing: ListingEntity, event: DealEventEntity, approval_type: ApprovalType
) -> QueueItemResponse:
    return QueueItemResponse(
        id=listing.id,
        listing_id=listing.id,
        listing_code=listing.code,
        approval_type=approval_type.value,
        transaction_type=listing.transaction_type.value,
        title=listing.title,
        price=listing.price,
        status=listing.status.value,
        created_at=event.created_at,
        customer_name=event.customer_name,
        customer_phone=event.customer_phone,
        deposit_amount=event.deposit_amount,
        event_notes=event.notes,
        deal_event=DealEventInfo(
            event_type=event.event_type.value,
            notes=event.notes,
            customer_name=event.customer_name,
            customer_phone=event.customer_phone,
            deposit_amount=event.deposit_amount,
            created_at=event.created_at,
        ),
        reported_by=_reporter_from_user(event.reported_by) if event.reported_by else None,
        **_map_listing_fields(listing),
    )


def _reporter_from_user(user: UserEntity) -> ReporterInfo:
    return ReporterInfo(
        id=user.id,
        full_name=user.full_name,
        email=user.email or "",
    )


def approval_to_response(item: dict) -> ApproveResponse:
    return ApproveResponse(
        id=item["id"],
        listing_id=item["listing_id"],
        listing_code=item["listing_code"],
        approval_type=item["approval_type"].value,
        decision=item["decision"].value,
        listing_status=item["listing_status"].value,
        created_at=item["created_at"],
    )
