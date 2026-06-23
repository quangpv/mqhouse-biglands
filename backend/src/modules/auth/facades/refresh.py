import hashlib
import uuid
from datetime import datetime, timezone

from fastapi import Depends, Body

from src.data.repositories.refresh_token_repo import RefreshTokenRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import RefreshTokenRequest, RefreshTokenResponse
from src.platform.security import create_jwt, create_refresh_jwt, decode_jwt
from src.shared.errors.exceptions import UnauthorizedError


async def refresh(
    data: RefreshTokenRequest = Body(...),
    repo: UserRepo = Depends(UserRepo),
    refresh_repo: RefreshTokenRepo = Depends(RefreshTokenRepo),
) -> RefreshTokenResponse:
    payload = decode_jwt(data.refresh_token)
    if payload.get("purpose") != "refresh":
        raise UnauthorizedError("Invalid refresh token")

    jti = payload.get("jti")
    user_id = payload.get("sub")
    if jti is None or user_id is None:
        raise UnauthorizedError("Invalid refresh token")

    jti_hash = hashlib.sha256(jti.encode()).hexdigest()
    stored = await refresh_repo.get_by_token_hash(jti_hash)
    if stored is None or stored.is_revoked:
        raise UnauthorizedError("Refresh token has been revoked")

    user = await repo.get(uuid.UUID(user_id))
    if user is None:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise UnauthorizedError("Account is deactivated")

    await refresh_repo.revoke(stored.id)

    new_access = create_jwt(user.id, user.role.value)
    new_refresh = create_refresh_jwt(user.id, user.role.value)
    new_payload = decode_jwt(new_refresh)
    new_hash = hashlib.sha256(new_payload["jti"].encode()).hexdigest()
    exp_timestamp = new_payload["exp"]
    expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    await refresh_repo.add(user.id, new_hash, expires_at)

    return RefreshTokenResponse(access_token=new_access, refresh_token=new_refresh)
