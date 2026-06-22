from math import ceil

from fastapi import Depends, Query

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
    transaction_type: str | None = Query(default=None),
    q: str | None = None,
    current_user: UserEntity = Depends(get_current_user),
    repo: NotificationRepo = Depends(NotificationRepo),
) -> NotificationListResponse:
    pagination = PaginationParams(page=page, size=per_page)
    items, total = await repo.list_by_user(
        user_id=current_user.id,
        page=pagination.page,
        per_page=pagination.size,
        is_read=is_read,
        transaction_type=transaction_type,
        search=q,
    )
    unread_count = await repo.get_unread_count(user_id=current_user.id)
    category_counts = await repo.get_category_counts(user_id=current_user.id)
    return NotificationListResponse(
        data=[notification_to_response(n) for n in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        total_pages=ceil(total / pagination.size) if pagination.size > 0 else 0,
        unread_count=unread_count,
        category_counts=category_counts,
    )
