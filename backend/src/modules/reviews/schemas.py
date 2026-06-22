import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.shared.pagination import PaginatedResponse
class CreateReviewRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class ReviewImageResponse(BaseModel):
    id: uuid.UUID
    url: str
    order: int


class ReviewResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    author_id: uuid.UUID
    author_name: str
    content: str
    images: list[ReviewImageResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReviewListResponse(PaginatedResponse):
    data: list[ReviewResponse]
