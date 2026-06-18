from src.data.notifications import DEFAULT_PREFS
from src.modules.user_settings.schemas import NotificationPreferencesResponse


def prefs_to_response(prefs: dict | None) -> NotificationPreferencesResponse:
    merged = {**DEFAULT_PREFS, **(prefs or {})}
    return NotificationPreferencesResponse(**merged)
