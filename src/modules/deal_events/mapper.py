from src.data.entities.deal_event import DealEventEntity
from src.modules.deal_events.schemas import DealEventResponse


def deal_event_to_response(entity: DealEventEntity) -> DealEventResponse:
    return DealEventResponse(
        id=entity.id,
        listing_id=entity.listing_id,
        event_type=entity.event_type.value,
        reported_by_id=entity.reported_by_id,
        confirmed_by_id=entity.confirmed_by_id,
        confirmed_at=entity.confirmed_at,
        notes=entity.notes,
        customer_name=entity.customer_name,
        customer_phone=entity.customer_phone,
        deposit_amount=entity.deposit_amount,
        created_at=entity.created_at,
    )
