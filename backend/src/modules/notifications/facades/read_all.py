from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.schemas import ReadAllResponse
from src.platform.auth import get_current_user


async def read_all(
    repo: NotificationRepo = Depends(NotificationRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ReadAllResponse:
    await repo.mark_all_read(current_user.id)
    return ReadAllResponse(message="All notifications marked as read")
