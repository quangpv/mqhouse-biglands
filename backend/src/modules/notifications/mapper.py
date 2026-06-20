from src.data.entities.notification import NotificationEntity
from src.modules.notifications.schemas import NotificationResponse


def notification_to_response(entity: NotificationEntity) -> NotificationResponse:
    return NotificationResponse(
        id=entity.id,
        user_id=entity.user_id,
        title=entity.title,
        body=entity.body,
        reference_type=entity.reference_type.value if entity.reference_type else None,
        reference_id=entity.reference_id,
        is_read=entity.is_read,
        created_at=entity.created_at,
    )
