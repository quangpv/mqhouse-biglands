import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity
from src.data.repositories.hot_property_repo import HotPropertyRepo
from src.data.repositories.property_repo import PropertyRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def remove_from_hot(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: HotPropertyRepo = Depends(HotPropertyRepo),
    prop_repo: PropertyRepo = Depends(PropertyRepo),
    _current_user: UserEntity = Depends(get_current_user),
) -> None:
    hot_prop = await repo.get_by_property(property_id)
    if hot_prop is None:
        raise NotFoundError("Property is not hot")

    prop = await prop_repo.get(property_id)
    if prop is not None:
        prop.is_hot = False
        prop.hot_order = None
        await prop_repo.save(prop)

    await repo.delete(hot_prop)
