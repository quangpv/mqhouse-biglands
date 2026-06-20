import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.mapper import notification_to_response
from src.modules.notifications.schemas import NotificationResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def mark_read(
    notification_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: NotificationRepo = Depends(NotificationRepo),
) -> NotificationResponse:
    notification = await repo.get_by_id(notification_id)
    if notification is None:
        raise NotFoundError("Notification not found")
    if notification.user_id != current_user.id:
        raise ForbiddenError("You can only mark your own notifications as read")

    notification = await repo.mark_read(notification_id)
    if notification is None:
        raise NotFoundError("Notification not found")
    return notification_to_response(notification)
