import uuid
from pathlib import Path

from fastapi import Depends, File, Form, HTTPException, UploadFile, status

from src.data.entities.file import EntityType, FileEntity
from src.data.entities.user import UserEntity
from src.data.repositories.file_repo import FileRepo
from src.modules.files.schemas import FileUploadResponse
from src.platform.auth import get_current_user
from src.platform.config import settings
from src.shared.errors.exceptions import BadRequestError

MAX_FILE_COUNT = 10


async def upload_files(
    files: list[UploadFile] = File(...),
    entity_type: EntityType | None = Form(None),
    repo: FileRepo = Depends(FileRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> FileUploadResponse:
    if not files:
        raise BadRequestError("At least one file is required")
    if len(files) > MAX_FILE_COUNT:
        raise BadRequestError(f"Maximum {MAX_FILE_COUNT} files allowed")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    file_ids: list[uuid.UUID] = []
    for file in files:
        content = await file.read()
        if len(content) > max_bytes:
            raise BadRequestError(
                f"File '{file.filename}' exceeds {settings.max_upload_size_mb}MB"
            )

        ext = Path(file.filename).suffix if file.filename else ""
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = upload_dir / unique_name

        file_path.write_bytes(content)

        entity = FileEntity(
            origin_name=file.filename or "unknown",
            path=str(file_path),
            mimetype=file.content_type or "application/octet-stream",
            size=len(content),
            entity_type=entity_type,
            created_by_id=current_user.id,
        )
        entity = await repo.save(entity)
        file_ids.append(entity.id)

    return FileUploadResponse(file_ids=file_ids)
