import uuid

from fastapi import Depends, Query

from src.data.entities.user import UserRole
from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import entity_to_response
from src.modules.users.schemas import PageDTO, UserListData


async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: UserRole | None = Query(None),
    is_active: bool | None = Query(None),
    search: str | None = Query(None),
    organization_id: uuid.UUID | None = Query(None),
    repo: UserRepo = Depends(UserRepo),
) -> UserListData:
    entities, total = await repo.search(
        role=role,
        is_active=is_active,
        search=search,
        organization_id=organization_id,
        page=page,
        size=size,
    )

    total_pages = (total + size - 1) // size

    return UserListData(
        data=[entity_to_response(e) for e in entities],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
