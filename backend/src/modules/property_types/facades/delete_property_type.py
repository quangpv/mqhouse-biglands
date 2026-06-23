import uuid

from fastapi import Depends

from src.data.repositories.property_type_repo import PropertyTypeRepo
from src.shared.errors.exceptions import NotFoundError


async def delete_property_type(
    entity_id: uuid.UUID,
    repo: PropertyTypeRepo = Depends(PropertyTypeRepo),
) -> None:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Property type not found")
    await repo.delete(entity)
