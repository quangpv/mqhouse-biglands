import uuid

from fastapi import Depends

from src.data.repositories.property_type_repo import PropertyTypeRepo
from src.modules.property_types.mapper import apply_to_entity, entity_to_response
from src.modules.property_types.schemas import (
    PropertyTypeResponse,
    UpdatePropertyTypeRequest,
)
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def update_property_type(
    entity_id: uuid.UUID,
    body: UpdatePropertyTypeRequest,
    repo: PropertyTypeRepo = Depends(PropertyTypeRepo),
) -> PropertyTypeResponse:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Property type not found")

    if body.code != entity.code:
        existing = await repo.get_by_code(body.code)
        if existing:
            raise ConflictError(f"Property type with code '{body.code}' already exists")

    entity = apply_to_entity(entity, body)
    await repo.save(entity)
    return entity_to_response(entity)
