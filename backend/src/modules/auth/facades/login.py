import hashlib
from datetime import datetime, timezone

from fastapi import Depends, Body

from src.data.repositories.refresh_token_repo import RefreshTokenRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import LoginRequest, LoginResponse
from src.platform.security import create_jwt, create_refresh_jwt, decode_jwt, verify_password
from src.shared.errors.exceptions import UnauthorizedError


async def login(
    data: LoginRequest = Body(...),
    repo: UserRepo = Depends(UserRepo),
    refresh_repo: RefreshTokenRepo = Depends(RefreshTokenRepo),
) -> LoginResponse:
    user = await repo.get_by_username(data.username)
    if user is None:
        raise UnauthorizedError("Invalid credentials")
    if not user.is_active:
        raise UnauthorizedError("Account is deactivated")
    if not verify_password(data.password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")

    access_token = create_jwt(user.id, user.role.value)
    refresh_token = create_refresh_jwt(user.id, user.role.value)

    payload = decode_jwt(refresh_token)
    jti_hash = hashlib.sha256(payload["jti"].encode()).hexdigest()
    exp_timestamp = payload["exp"]
    expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    await refresh_repo.add(user.id, jti_hash, expires_at)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)
