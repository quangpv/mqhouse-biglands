from fastapi import Depends

from src.data.repositories.property_type_repo import PropertyTypeRepo
from src.modules.property_types.mapper import entity_to_response, request_to_entity
from src.modules.property_types.schemas import (
    CreatePropertyTypeRequest,
    PropertyTypeResponse,
)
from src.shared.errors.exceptions import ConflictError


async def create_property_type(
    body: CreatePropertyTypeRequest,
    repo: PropertyTypeRepo = Depends(PropertyTypeRepo),
) -> PropertyTypeResponse:
    existing = await repo.get_by_code(body.code)
    if existing:
        raise ConflictError(f"Property type with code '{body.code}' already exists")

    entity = request_to_entity(body)
    entity = await repo.save(entity)
    return entity_to_response(entity)
