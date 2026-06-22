from datetime import datetime, timedelta, timezone

from fastapi import Depends
from jose import jwt

from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import ForgotPasswordRequest, ForgotPasswordResponse
from src.platform.config import settings
from src.shared.errors.exceptions import NotFoundError


async def forgot_password(
    data: ForgotPasswordRequest,
    repo: UserRepo = Depends(UserRepo),
) -> ForgotPasswordResponse:
    user = await repo.get_by_username(data.username)
    if user is None:
        raise NotFoundError("User not found")

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "purpose": "password_reset",
        "iat": now,
        "exp": now + timedelta(minutes=15),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    return ForgotPasswordResponse(token=token, message="Password reset token generated. Please check your email.")
