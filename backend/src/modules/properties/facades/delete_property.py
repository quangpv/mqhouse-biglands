import uuid

from fastapi import Depends, Path

from src.data.entities.property import PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.property_repo import PropertyRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def delete_property(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> dict:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if current_user.role == UserRole.SALE:
        if entity.created_by_id != current_user.id:
            raise ForbiddenError("Only the owner can delete this property")

    hard_deletable = (
        PropertyStatus.DRAFT,
        PropertyStatus.POST_PENDING,
        PropertyStatus.AVAILABLE,
    )
    if entity.status in hard_deletable:
        await repo.delete(entity)
    else:
        from datetime import datetime
        entity.deleted_at = datetime.now()
        await repo.save(entity)

    return {"success": True}
