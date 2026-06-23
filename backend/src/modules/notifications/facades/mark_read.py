import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.mapper import entity_to_response
from src.modules.notifications.schemas import NotificationResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def mark_read(
    notification_id: uuid.UUID = Path(..., alias="id"),
    repo: NotificationRepo = Depends(NotificationRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> NotificationResponse:
    entity = await repo.get(notification_id)
    if not entity:
        raise NotFoundError("Notification not found")
    if entity.user_id != current_user.id:
        raise ForbiddenError("You can only mark your own notifications as read")

    entity = await repo.mark_read(notification_id)
    assert entity is not None
    return entity_to_response(entity)
