from fastapi import Depends, Query

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.mapper import entity_to_response
from src.modules.notifications.schemas import NotificationListResponse, PageDTO
from src.platform.auth import get_current_user


async def list_notifications(
    is_read: bool | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    repo: NotificationRepo = Depends(NotificationRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> NotificationListResponse:
    rows, total, total_pages = await repo.list_by_user(
        user_id=current_user.id,
        is_read=is_read,
        page=page,
        size=size,
    )
    return NotificationListResponse(
        data=[entity_to_response(r) for r in rows],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
