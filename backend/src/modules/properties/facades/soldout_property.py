import uuid

from fastapi import Depends, Path

from src.data.entities.approval import ApprovalEntity, ApprovalStatus
from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import NotesRequest, PropertyResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def soldout_property(
    body: NotesRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status not in (PropertyStatus.AVAILABLE, PropertyStatus.DEPOSITED):
        raise ForbiddenError("Only available or deposited properties can be marked as sold out")

    if current_user.role == UserRole.SALE:
        new_status = PropertyStatus.SOLDOUT_PENDING
    elif current_user.role in (UserRole.ADMIN, UserRole.APPROVER):
        new_status = PropertyStatus.SOLDOUT
    else:
        raise ForbiddenError("Insufficient permissions")

    old_status = entity.status
    entity.status = new_status
    entity = await repo.save(entity)

    transition = await repo.create_transition(
        property_id=property_id,
        from_status=old_status,
        to_status=new_status,
        action=Action.SOLDOUT,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
        notes=body.notes,
    )

    if current_user.role == UserRole.SALE:
        approval = ApprovalEntity(
            property_id=entity.id,
            transition_id=transition.id,
            transaction_type_id=entity.transaction_type_id,
            status=ApprovalStatus.PENDING,
        )
        await approval_repo.save(approval)

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
