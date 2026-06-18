from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.schemas import UnreadCountResponse
from src.platform.auth import get_current_user


async def get_unread_count(
    current_user: UserEntity = Depends(get_current_user),
    repo: NotificationRepo = Depends(NotificationRepo),
) -> UnreadCountResponse:
    count = await repo.get_unread_count(current_user.id)
    return UnreadCountResponse(count=count)
