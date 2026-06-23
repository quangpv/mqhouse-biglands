from datetime import datetime, timezone

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.refresh_token_repo import RefreshTokenRepo
from src.data.repositories.token_blacklist_repo import TokenBlacklistRepo
from src.modules.auth.schemas import LogoutResponse
from src.platform.auth import get_current_user


async def logout(
    current_user: UserEntity = Depends(get_current_user),
    blacklist_repo: TokenBlacklistRepo = Depends(TokenBlacklistRepo),
    refresh_repo: RefreshTokenRepo = Depends(RefreshTokenRepo),
) -> LogoutResponse:
    jti = current_user._jti
    exp = current_user._exp
    if jti and exp:
        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        await blacklist_repo.add(jti, expires_at)

    await refresh_repo.revoke_all_for_user(current_user.id)

    return LogoutResponse(message="Logged out successfully")
