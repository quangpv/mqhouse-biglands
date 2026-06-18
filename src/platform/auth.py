import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.platform.security import decode_jwt
from src.shared.errors.exceptions import ForbiddenError, UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    repo: UserRepo = Depends(UserRepo),
) -> UserEntity:
    if credentials is None:
        raise UnauthorizedError("Missing authorization header")

    payload = decode_jwt(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedError("Invalid or expired token")

    user = await repo.get(uuid.UUID(user_id))
    if user is None:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise UnauthorizedError("User is deactivated")

    return user


def require_role(*roles: str):
    async def role_checker(current_user: UserEntity = Depends(get_current_user)) -> UserEntity:
        if current_user.role.value not in roles:
            raise ForbiddenError(f"Requires one of {', '.join(roles)}")
        return current_user

    return role_checker
