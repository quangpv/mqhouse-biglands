from fastapi import APIRouter, Depends, status

from src.modules.notifications.facades.list_notifications import list_notifications
from src.modules.notifications.facades.get_unread_count import get_unread_count
from src.modules.notifications.facades.mark_read import mark_read
from src.modules.notifications.facades.mark_all_read import mark_all_read
from src.modules.notifications.schemas import NotificationListResponse, NotificationResponse, UnreadCountResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def list_all(result: NotificationListResponse = Depends(list_notifications)):
    return result


@router.get("/unread-count", response_model=UnreadCountResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def unread_count(result: UnreadCountResponse = Depends(get_unread_count)):
    return result


@router.patch("/{notification_id}/read", response_model=NotificationResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def mark_one_read(result: NotificationResponse = Depends(mark_read)):
    return result


@router.post("/read-all", response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def read_all(result: dict = Depends(mark_all_read)):
    return result
