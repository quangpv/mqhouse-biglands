from math import ceil

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.mapper import notification_to_response
from src.modules.notifications.schemas import NotificationListResponse
from src.platform.auth import get_current_user
from src.shared.pagination import PaginationParams


async def list_notifications(
    page: int = 1,
    per_page: int = 20,
    is_read: bool | None = None,
    current_user: UserEntity = Depends(get_current_user),
    repo: NotificationRepo = Depends(NotificationRepo),
) -> NotificationListResponse:
    pagination = PaginationParams(page=page, size=per_page)
    items, total = await repo.list_by_user(
        user_id=current_user.id,
        page=pagination.page,
        per_page=pagination.size,
        is_read=is_read,
    )
    return NotificationListResponse(
        data=[notification_to_response(n) for n in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        total_pages=ceil(total / pagination.size) if pagination.size > 0 else 0,
    )
