from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.user_settings.mapper import prefs_to_response
from src.modules.user_settings.schemas import NotificationPreferencesResponse
from src.platform.auth import get_current_user
from src.platform.dependencies import get_db


async def update_notification_preferences(
    data: NotificationPreferencesResponse,
    current_user: UserEntity = Depends(get_current_user),
    repo: UserRepo = Depends(UserRepo),
    db: AsyncSession = Depends(get_db),
) -> NotificationPreferencesResponse:
    current_user.notification_prefs = data.model_dump()
    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)
    return prefs_to_response(current_user.notification_prefs)
