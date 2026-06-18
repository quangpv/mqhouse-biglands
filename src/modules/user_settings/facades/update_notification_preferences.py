from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.user_settings.mapper import prefs_to_response
from src.modules.user_settings.schemas import NotificationPreferencesResponse
from src.platform.auth import get_current_user


async def update_notification_preferences(
    data: NotificationPreferencesResponse,
    current_user: UserEntity = Depends(get_current_user),
    repo: UserRepo = Depends(UserRepo),
) -> NotificationPreferencesResponse:
    current_user.notification_prefs = data.model_dump()
    await repo.save(current_user)
    return prefs_to_response(current_user.notification_prefs)
