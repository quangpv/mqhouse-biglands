from fastapi import Depends, Query

from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import UserListResponse, UserResponse
from src.shared.pagination import build_paginated_response


async def list_users(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    repo: UserRepo = Depends(UserRepo),
) -> UserListResponse:
    query = repo.build_list_query(search=search, role=role, is_active=is_active)
    rows, total = await repo.paginated_list(query, page=page, size=size)
    items = [user_to_response(u) for u in rows]
    return UserListResponse(**build_paginated_response(items, page, size, total).model_dump())
