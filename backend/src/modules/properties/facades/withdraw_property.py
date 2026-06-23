import uuid

from fastapi import Depends, Path

from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import NotesRequest, PropertyResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def withdraw_property(
    body: NotesRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status != PropertyStatus.POST_PENDING:
        raise ForbiddenError("Only properties in post_pending status can be withdrawn")

    if current_user.role == UserRole.SALE:
        if entity.created_by_id != current_user.id:
            raise ForbiddenError("Only the owner can withdraw this property")

    old_status = entity.status
    entity.status = PropertyStatus.DRAFT
    entity = await repo.save(entity)

    await repo.create_transition(
        property_id=property_id,
        from_status=old_status,
        to_status=PropertyStatus.DRAFT,
        action=Action.WITHDRAW,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
        notes=body.notes,
    )

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
