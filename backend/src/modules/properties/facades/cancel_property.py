import uuid

from fastapi import Depends, Path

from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import NotesRequest, PropertyResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def cancel_property(
    body: NotesRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status != PropertyStatus.DEPOSITED:
        raise ForbiddenError("Only deposited properties can be cancelled")

    if current_user.role == UserRole.SALE:
        new_status = PropertyStatus.CANCEL_PENDING
    elif current_user.role in (UserRole.ADMIN, UserRole.APPROVER):
        new_status = PropertyStatus.AVAILABLE
    else:
        raise ForbiddenError("Insufficient permissions")

    old_status = entity.status
    entity.status = new_status
    entity = await repo.save(entity)

    await repo.create_transition(
        property_id=property_id,
        from_status=old_status,
        to_status=new_status,
        action=Action.CANCEL,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
        notes=body.notes,
    )

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
