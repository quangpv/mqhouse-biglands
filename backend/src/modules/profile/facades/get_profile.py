from fastapi import Depends

from src.data.entities.user import UserEntity
from src.modules.users.mapper import entity_to_response
from src.modules.users.schemas import UserResponse
from src.platform.auth import get_current_user


async def get_profile(
    current_user: UserEntity = Depends(get_current_user),
) -> UserResponse:
    return entity_to_response(current_user)
