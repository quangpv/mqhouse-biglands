import uuid

from fastapi import Depends, Path

from src.data.entities.property import PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import apply_to_entity, entity_to_response
from src.modules.properties.schemas import PropertyResponse, UpdatePropertyRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def update_property(
    body: UpdatePropertyRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status not in (
        PropertyStatus.DRAFT,
        PropertyStatus.POST_PENDING,
        PropertyStatus.AVAILABLE,
    ):
        raise ForbiddenError("Property cannot be updated in current status")

    if current_user.role == UserRole.SALE:
        if entity.created_by_id != current_user.id:
            raise ForbiddenError("Only the owner can update this property")
        previous = entity.status
        entity.status = PropertyStatus.EDIT_PENDING
        entity.previous_status = previous
    elif current_user.role in (UserRole.ADMIN, UserRole.APPROVER):
        if entity.previous_status is not None:
            entity.status = entity.previous_status
            entity.previous_status = None

    apply_to_entity(entity, body)

    if body.image_ids is not None:
        current_ids = await repo.get_file_ids_in_property(property_id)
        for fid in body.image_ids:
            if fid not in current_ids:
                await repo.create_image(property_id, fid, order=len(current_ids))

    entity = await repo.save(entity)
    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
