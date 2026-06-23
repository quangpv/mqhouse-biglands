from fastapi import Depends, Body

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import ChangePasswordRequest, ChangePasswordResponse
from src.platform.auth import get_current_user
from src.platform.security import hash_password, verify_password
from src.shared.errors.exceptions import BadRequestError


async def change_password(
    data: ChangePasswordRequest = Body(...),
    current_user: UserEntity = Depends(get_current_user),
    repo: UserRepo = Depends(UserRepo),
) -> ChangePasswordResponse:
    if not verify_password(data.current_password, current_user.password_hash):
        raise BadRequestError("Current password is incorrect")

    current_user.password_hash = hash_password(data.new_password)
    await repo.save(current_user)

    return ChangePasswordResponse(message="Password changed successfully")
