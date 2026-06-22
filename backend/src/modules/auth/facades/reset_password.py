import uuid

from fastapi import Depends
from jose import JWTError, jwt

from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import ResetPasswordRequest, ResetPasswordResponse
from src.platform.config import settings
from src.platform.security import hash_password
from src.shared.errors.exceptions import BadRequestError


async def reset_password(
    data: ResetPasswordRequest,
    repo: UserRepo = Depends(UserRepo),
) -> ResetPasswordResponse:
    try:
        payload = jwt.decode(data.token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise BadRequestError("Invalid or expired reset token")

    if payload.get("purpose") != "password_reset":
        raise BadRequestError("Invalid token purpose")

    user_id = payload.get("sub")
    if user_id is None:
        raise BadRequestError("Invalid token payload")

    user = await repo.get(uuid.UUID(user_id))
    if user is None:
        raise BadRequestError("User not found")

    user.password_hash = hash_password(data.new_password)
    await repo.save(user)

    return ResetPasswordResponse(message="Password reset successfully")
