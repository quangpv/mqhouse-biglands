from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.platform.auth import get_current_user


async def mark_all_read(
    current_user: UserEntity = Depends(get_current_user),
    repo: NotificationRepo = Depends(NotificationRepo),
) -> dict:
    count = await repo.mark_all_read(current_user.id)
    return {"updated": count}
