import uuid
from pathlib import Path

from fastapi import Depends

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.file_repo import FileRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def delete_file(
    file_id: uuid.UUID,
    repo: FileRepo = Depends(FileRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> None:
    entity = await repo.get(file_id)
    if entity is None:
        raise NotFoundError("File not found")

    is_owner = entity.created_by_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    if not is_owner and not is_admin:
        raise ForbiddenError("Only the owner or admin can delete this file")

    file_path = Path(entity.path)
    if file_path.exists():
        file_path.unlink()

    await repo.delete(entity)
