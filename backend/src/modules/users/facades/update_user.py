import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import apply_to_entity, entity_to_response
from src.modules.users.schemas import UpdateUserRequest, UserResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, ForbiddenError, NotFoundError


async def update_user(
    body: UpdateUserRequest,
    user_id: uuid.UUID = Path(..., alias="user_id"),
    repo: UserRepo = Depends(UserRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> UserResponse:
    entity = await repo.get(user_id)
    if not entity:
        raise NotFoundError("User not found")

    if body.email and body.email != entity.email:
        existing = await repo.get_by_email(body.email)
        if existing:
            raise ConflictError(f"User with email '{body.email}' already exists")

    if body.role is not None and current_user.id == user_id and body.role != entity.role:
        if entity.role == UserRole.ADMIN and body.role != UserRole.ADMIN:
            raise ForbiddenError("Cannot demote yourself from ADMIN")

    apply_to_entity(entity, body)
    entity = await repo.save(entity)

    return entity_to_response(entity)
