from src.data.entities.notification import NotificationEntity
from src.modules.notifications.schemas import NotificationResponse


def entity_to_response(entity: NotificationEntity) -> NotificationResponse:
    return NotificationResponse(
        id=entity.id,
        user_id=entity.user_id,
        title=entity.title,
        body=entity.body,
        reference_type=entity.reference_type,
        reference_id=entity.reference_id,
        is_read=entity.is_read,
        event_type=entity.event_type,
        actor_name=entity.actor_name,
        transaction_type=entity.transaction_type,
        created_at=entity.created_at,
    )
