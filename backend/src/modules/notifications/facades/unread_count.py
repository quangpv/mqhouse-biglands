from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.schemas import NotificationCountResponse
from src.platform.auth import get_current_user


async def unread_count(
    repo: NotificationRepo = Depends(NotificationRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> NotificationCountResponse:
    count = await repo.unread_count(current_user.id)
    return NotificationCountResponse(count=count)
