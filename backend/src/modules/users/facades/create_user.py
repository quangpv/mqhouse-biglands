from fastapi import BackgroundTasks, Depends

from src.data.repositories.user_repo import UserRepo
from src.modules.users.mapper import entity_to_response, request_to_entity
from src.modules.users.schemas import CreateUserRequest, UserResponse
from src.platform.dependencies import get_email_service
from src.platform.email import SmtpEmailService
from src.shared.errors.exceptions import ConflictError


async def create_user(
    bg_tasks: BackgroundTasks,
    body: CreateUserRequest,
    repo: UserRepo = Depends(UserRepo),
    email_service: SmtpEmailService = Depends(get_email_service),
) -> UserResponse:
    existing = await repo.get_by_username(body.username)
    if existing:
        raise ConflictError(f"User with username '{body.username}' already exists")

    if body.email:
        existing = await repo.get_by_email(body.email)
        if existing:
            raise ConflictError(f"User with email '{body.email}' already exists")

    entity = request_to_entity(body)
    entity = await repo.save(entity)

    if body.email:
        bg_tasks.add_task(email_service.send_welcome, body.email, body.username, body.password)

    return entity_to_response(entity)
