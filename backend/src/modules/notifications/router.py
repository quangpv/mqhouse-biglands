from fastapi import APIRouter, Depends, status

from src.modules.notifications.facades.list_notifications import list_notifications
from src.modules.notifications.facades.mark_read import mark_read
from src.modules.notifications.facades.read_all import read_all
from src.modules.notifications.facades.unread_count import unread_count
from src.modules.notifications.schemas import (
    NotificationCountResponse,
    NotificationListResponse,
    NotificationResponse,
    ReadAllResponse,
)
from src.platform.auth import require_auth

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get(
    "",
    response_model=NotificationListResponse,
    dependencies=[Depends(require_auth)],
)
async def list_notifications_endpoint(
    result: NotificationListResponse = Depends(list_notifications),
):
    return result


@router.get(
    "/unread-count",
    response_model=NotificationCountResponse,
    dependencies=[Depends(require_auth)],
)
async def unread_count_endpoint(
    result: NotificationCountResponse = Depends(unread_count),
):
    return result


@router.patch(
    "/{id}/read",
    response_model=NotificationResponse,
    dependencies=[Depends(require_auth)],
)
async def mark_read_endpoint(
    result: NotificationResponse = Depends(mark_read),
):
    return result


@router.post(
    "/read-all",
    response_model=ReadAllResponse,
    dependencies=[Depends(require_auth)],
)
async def read_all_endpoint(
    result: ReadAllResponse = Depends(read_all),
):
    return result
