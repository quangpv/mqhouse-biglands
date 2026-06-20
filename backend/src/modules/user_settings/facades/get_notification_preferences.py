from fastapi import Depends

from src.data.entities.user import UserEntity
from src.modules.user_settings.mapper import prefs_to_response
from src.modules.user_settings.schemas import NotificationPreferencesResponse
from src.platform.auth import get_current_user


async def get_notification_preferences(
    current_user: UserEntity = Depends(get_current_user),
) -> NotificationPreferencesResponse:
    return prefs_to_response(current_user.notification_prefs)
