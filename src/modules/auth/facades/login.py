from fastapi import Depends, Body

from src.data.repositories.user_repo import UserRepo
from src.modules.auth.schemas import LoginRequest, LoginResponse
from src.platform.security import create_jwt, verify_password
from src.shared.errors.exceptions import UnauthorizedError


async def login(
    data: LoginRequest = Body(...),
    repo: UserRepo = Depends(UserRepo),
) -> LoginResponse:
    user = await repo.get_by_username(data.username)
    if user is None:
        raise UnauthorizedError("Invalid credentials")
    if not user.is_active:
        raise UnauthorizedError("Account is deactivated")
    if not verify_password(data.password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")

    token = create_jwt(user.id, user.role.value)
    return LoginResponse(access_token=token)
