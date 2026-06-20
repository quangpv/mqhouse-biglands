from src.data.entities.approval import ApprovalType
from src.data.entities.deal_event import DealEventEntity
from src.data.entities.listing import ListingEntity
from src.modules.approvals.schemas import ApproveResponse, QueueItemResponse


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
