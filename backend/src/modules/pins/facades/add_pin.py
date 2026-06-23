import uuid

from fastapi import Depends, Path

from src.data.entities.pin import PinEntity
from src.data.entities.user import UserEntity
from src.data.repositories.pin_repo import PinRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.pins.mapper import entity_to_pin_response
from src.modules.pins.schemas import PinResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def add_pin(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PinRepo = Depends(PinRepo),
    prop_repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PinResponse:
    prop = await prop_repo.get(property_id)
    if prop is None:
        raise NotFoundError("Property not found")

    existing = await repo.get(current_user.id, property_id)
    if existing is not None:
        raise ConflictError("Property already pinned")

    entity = PinEntity(user_id=current_user.id, property_id=property_id)
    entity = await repo.save(entity)
    return entity_to_pin_response(entity)
