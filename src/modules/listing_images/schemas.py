import uuid

from pydantic import BaseModel


class ReorderImagesRequest(BaseModel):
    image_ids: list[uuid.UUID]


class ImageResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    url: str
    order: int
    is_primary: bool | None = False
