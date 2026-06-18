from pydantic import BaseModel

from src.data.repositories.notification_repo import DEFAULT_PREFS


class NotificationPreferencesResponse(BaseModel):
    listing_post_created: bool = True
    listing_post_approved: bool = True
    listing_post_rejected: bool = True
    deposit_reported: bool = True
    deposit_confirmed: bool = True
    deposit_rejected: bool = True
    closure_reported: bool = True
    closure_confirmed: bool = True
    closure_rejected: bool = True
    cancellation_reported: bool = True
    cancellation_confirmed: bool = True
    cancellation_rejected: bool = True
    sold_out_reported: bool = True
    sold_out_confirmed: bool = True
    listing_expired: bool = True
