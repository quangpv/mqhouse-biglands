import uuid

from fastapi import Depends, HTTPException, status

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.user_repo import UserRepo
from src.platform.auth import get_current_user
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import UserResponse
from src.shared.errors.exceptions import NotFoundError


async def deactivate_user(
    user_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: UserRepo = Depends(UserRepo),
) -> UserResponse:
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot deactivate yourself")

    user = await repo.get(user_id)
    if user is None:
        raise NotFoundError("User not found")

    if user.role == UserRole.ADMIN:
        admin_count = await repo.count_active_admins()
        if admin_count <= 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot deactivate the last active admin")

    user.is_active = False
    user = await repo.save(user)
    return user_to_response(user)
