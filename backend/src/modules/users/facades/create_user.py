import secrets
import string
import uuid

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.data.entities.user import UserEntity
from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import user_to_response
from src.modules.users.schemas import CreateUserRequest, UserResponse
from src.platform.auth import get_current_user
from src.platform.security import hash_password
from src.shared.errors.exceptions import ConflictError


def _generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def create_user(
    data: CreateUserRequest,
    repo: UserRepo = Depends(UserRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> UserResponse:
    password = data.password or _generate_password()
    user = UserEntity(
        full_name=data.full_name,
        username=data.username,
        phone=data.phone,
        email=data.email,
        password_hash=hash_password(password),
        role=data.role,
        is_active=True,
        organization_id=uuid.UUID(data.organization_id) if data.organization_id else None,
        created_by_id=current_user.id,
    )
    try:
        user = await repo.create(user)
    except IntegrityError:
        raise ConflictError("Username already exists")

    return user_to_response(user, generated_password=password if data.password is None else None)
