from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import CreateUserRequest, UserResponse
from src.platform.security import hash_password


async def create_user(
    data: CreateUserRequest,
    repo: UserRepo = Depends(UserRepo),
) -> UserResponse:
    user = UserEntity(
        full_name=data.full_name,
        username=data.username,
        phone=data.phone,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        is_active=True,
    )
    try:
        user = await repo.create(user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    return user_to_response(user)
