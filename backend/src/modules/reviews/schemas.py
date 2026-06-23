import uuid
from datetime import datetime

from pydantic import BaseModel


class FileInfo(BaseModel):
    id: uuid.UUID
    origin_name: str
    path: str
    mimetype: str
    created_by: uuid.UUID
    entity_type: str
    size: int


class PageDTO(BaseModel):
    page: int
    size: int
    total_pages: int


class CreateReviewRequest(BaseModel):
    content: str
    file_ids: list[uuid.UUID] = []


class ReviewResponse(BaseModel):
    id: uuid.UUID
    property_id: uuid.UUID
    author_id: uuid.UUID
    author_name: str
    content: str
    images: list[FileInfo] = []
    created_at: datetime
    updated_at: datetime


class ReviewListResponse(BaseModel):
    data: list[ReviewResponse]
    metadata: PageDTO
