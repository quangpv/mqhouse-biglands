import uuid
from datetime import datetime

from pydantic import BaseModel

from src.data.entities.file import EntityType


class FileInfoResponse(BaseModel):
    id: uuid.UUID
    origin_name: str
    path: str
    mimetype: str
    created_by: uuid.UUID
    entity_type: EntityType | None = None
    size: int
    created_at: datetime
    updated_at: datetime


class FileUploadResponse(BaseModel):
    file_ids: list[uuid.UUID]
