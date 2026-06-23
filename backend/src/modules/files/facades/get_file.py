import uuid

from fastapi import Depends

from src.data.repositories.file_repo import FileRepo
from src.modules.files.mapper import file_entity_to_response
from src.modules.files.schemas import FileInfoResponse
from src.shared.errors.exceptions import NotFoundError


async def get_file(
    file_id: uuid.UUID,
    repo: FileRepo = Depends(FileRepo),
) -> FileInfoResponse:
    entity = await repo.get(file_id)
    if entity is None:
        raise NotFoundError("File not found")
    return file_entity_to_response(entity)
