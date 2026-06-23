import uuid

from fastapi import Depends, Path

from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import entity_to_response
from src.modules.users.schemas import UserResponse
from src.shared.errors.exceptions import NotFoundError


async def reactivate_user(
    user_id: uuid.UUID = Path(..., alias="user_id"),
    repo: UserRepo = Depends(UserRepo),
) -> UserResponse:
    entity = await repo.get(user_id)
    if not entity:
        raise NotFoundError("User not found")

    entity.is_active = True
    entity = await repo.save(entity)

    return entity_to_response(entity)
