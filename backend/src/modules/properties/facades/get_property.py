import uuid

from fastapi import Depends, Path

from src.data.entities.property import PropertyStatus
from src.data.entities.user import UserEntity
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import PropertyResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def get_property(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status == PropertyStatus.DRAFT and entity.created_by_id != current_user.id:
        raise ForbiddenError("Draft properties are only visible to their owner")

    return entity_to_response(entity)
