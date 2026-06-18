from src.modules.approvals.schemas import ApproveResponse, QueueItemResponse


def queue_item_to_response(item: dict) -> QueueItemResponse:
    return QueueItemResponse(
        id=item["id"],
        listing_id=item["listing_id"],
        listing_code=item["listing_code"],
        approval_type=item["approval_type"].value,
        transaction_type=item["transaction_type"].value,
        title=item.get("title"),
        price=item.get("price"),
        status=item["status"].value if hasattr(item["status"], "value") else str(item["status"]),
        created_at=item["created_at"],
        customer_name=item.get("customer_name"),
        customer_phone=item.get("customer_phone"),
        deposit_amount=item.get("deposit_amount"),
        event_notes=item.get("event_notes"),
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
