import uuid

from fastapi import Depends

from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import UserResponse
from src.shared.errors.exceptions import NotFoundError


async def reactivate_user(
    user_id: uuid.UUID,
    repo: UserRepo = Depends(UserRepo),
) -> UserResponse:
    user = await repo.get(user_id)
    if user is None:
        raise NotFoundError("User not found")

    user.is_active = True
    user = await repo.save(user)
    return user_to_response(user)
