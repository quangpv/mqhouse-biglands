import uuid

from fastapi import Depends

from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import UpdateUserRequest, UserResponse
from src.platform.security import hash_password
from src.shared.errors.exceptions import NotFoundError


async def update_user(
    user_id: uuid.UUID,
    data: UpdateUserRequest,
    repo: UserRepo = Depends(UserRepo),
) -> UserResponse:
    user = await repo.get(user_id)
    if user is None:
        raise NotFoundError("User not found")

    if data.full_name is not None:
        user.full_name = data.full_name
    if data.phone is not None:
        user.phone = data.phone
    if data.email is not None:
        user.email = data.email
    if data.password is not None:
        user.password_hash = hash_password(data.password)

    user = await repo.save(user)
    return user_to_response(user)
