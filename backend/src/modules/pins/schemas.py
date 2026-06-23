from pydantic import BaseModel

from src.modules.properties.schemas import PageDTO, PropertyResponse


class PinResponse(BaseModel):
    message: str


class MyPinListResponse(BaseModel):
    data: list[PropertyResponse]
    metadata: PageDTO
