import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity
from src.data.repositories.pin_repo import PinRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def remove_pin(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PinRepo = Depends(PinRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> None:
    pin = await repo.get(current_user.id, property_id)
    if pin is None:
        raise NotFoundError("Property not pinned")
    await repo.delete(pin)
