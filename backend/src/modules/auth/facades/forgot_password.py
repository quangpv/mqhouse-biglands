from datetime import datetime, timedelta, timezone

from fastapi import Depends, Body
from jose import jwt

from src.data.repositories.user_repo import UserRepo
from src.platform.config import settings
from src.platform.dependencies import get_email_service
from src.platform.email import SmtpEmailService
from src.shared.errors.exceptions import NotFoundError
from src.modules.auth.schemas import ForgotPasswordRequest, ForgotPasswordResponse


async def forgot_password(
    data: ForgotPasswordRequest = Body(...),
    repo: UserRepo = Depends(UserRepo),
    email_service: SmtpEmailService = Depends(get_email_service),
) -> ForgotPasswordResponse:
    user = await repo.get_by_email(data.email)
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

    if not user.email:
        raise NotFoundError("User has no email address")

    await email_service.send_password_reset(user.email, token)

    return ForgotPasswordResponse(message="Password reset link sent to your email")
