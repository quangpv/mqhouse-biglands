import uuid

from fastapi import Depends

from src.data.repositories.property_type_repo import PropertyTypeRepo
from src.modules.property_types.mapper import entity_to_response
from src.modules.property_types.schemas import PropertyTypeResponse
from src.shared.errors.exceptions import NotFoundError


async def get_property_type(
    entity_id: uuid.UUID,
    repo: PropertyTypeRepo = Depends(PropertyTypeRepo),
) -> PropertyTypeResponse:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Property type not found")
    return entity_to_response(entity)
