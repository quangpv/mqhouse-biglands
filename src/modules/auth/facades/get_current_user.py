from fastapi import Depends

from src.data.entities.user import UserEntity
from src.modules.auth.mapper import user_to_response
from src.modules.auth.schemas import UserResponse
from src.platform.auth import get_current_user


async def get_current_user_facade(
    current_user: UserEntity = Depends(get_current_user),
) -> UserResponse:
    return user_to_response(current_user)
