import uuid

from fastapi import Body, Depends, Path

from src.data.entities.hot_property import HotPropertyEntity
from src.data.entities.user import UserEntity
from src.data.repositories.hot_property_repo import HotPropertyRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.hots.mapper import entity_to_response
from src.modules.hots.schemas import HotPropertyResponse, PromoteToHotRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def promote_to_hot(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    body: PromoteToHotRequest = Body(...),
    repo: HotPropertyRepo = Depends(HotPropertyRepo),
    prop_repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> HotPropertyResponse:
    prop = await prop_repo.get(property_id)
    if prop is None:
        raise NotFoundError("Property not found")

    existing = await repo.get_by_property(property_id)
    if existing is not None:
        raise ConflictError("Property is already hot")

    entity = HotPropertyEntity(
        property_id=property_id,
        start_time=body.start_time,
        end_time=body.end_time,
        created_by_id=current_user.id,
    )
    entity = await repo.save(entity)

    max_order = await prop_repo.get_max_hot_order()
    prop.is_hot = True
    prop.hot_order = (max_order or 0) + 1
    await prop_repo.save(prop)

    await repo.db.refresh(entity)
    return entity_to_response(entity)
