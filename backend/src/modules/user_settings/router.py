from fastapi import APIRouter, Depends

from src.modules.user_settings.facades.get_notification_preferences import get_notification_preferences
from src.modules.user_settings.facades.update_notification_preferences import update_notification_preferences
from src.modules.user_settings.schemas import NotificationPreferencesResponse
from src.platform.auth import require_role

router = APIRouter(tags=["user_settings"])


@router.get("/users/me/notification-preferences", response_model=NotificationPreferencesResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def get_prefs(result: NotificationPreferencesResponse = Depends(get_notification_preferences)):
    return result


@router.put("/users/me/notification-preferences", response_model=NotificationPreferencesResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def update_prefs(result: NotificationPreferencesResponse = Depends(update_notification_preferences)):
    return result
