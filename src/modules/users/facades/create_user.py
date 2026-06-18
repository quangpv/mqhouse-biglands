from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import CreateUserRequest, UserResponse
from src.platform.auth import get_current_user
from src.platform.security import hash_password


async def create_user(
    data: CreateUserRequest,
    repo: UserRepo = Depends(UserRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> UserResponse:
    user = UserEntity(
        full_name=data.full_name,
        username=data.username,
        phone=data.phone,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        is_active=True,
        created_by_id=current_user.id,
    )
    try:
        user = await repo.create(user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    return user_to_response(user)
