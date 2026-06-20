from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.data.repositories.token_blacklist_repo import TokenBlacklistRepo
from src.platform.security import decode_jwt
from src.shared.errors.exceptions import UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


async def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    blacklist_repo: TokenBlacklistRepo = Depends(TokenBlacklistRepo),
) -> None:
    if credentials is None:
        raise UnauthorizedError("Missing authorization header")
    payload = decode_jwt(credentials.credentials)
    jti = payload.get("jti")
    exp = payload.get("exp")
    if jti and exp:
        from datetime import datetime, timezone
        await blacklist_repo.add(jti, datetime.fromtimestamp(exp, tz=timezone.utc))
