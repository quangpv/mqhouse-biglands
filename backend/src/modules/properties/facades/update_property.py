import uuid
from decimal import Decimal
from enum import Enum as PyEnum

from fastapi import Depends, Path

from src.data.entities.approval import ApprovalEntity, ApprovalStatus
from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import apply_to_entity, entity_to_response
from src.modules.properties.schemas import PropertyResponse, UpdatePropertyRequest
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError
from src.shared.services.notification_service import NotificationService
from src.shared.utils.notification_formatter import format_notification_title


async def update_property(
    body: UpdatePropertyRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
    notif_service: NotificationService = Depends(NotificationService),
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
        action = Action.EDIT
        transition_from = entity.status
        transition_to = PropertyStatus.EDIT_PENDING
        needs_approval = True
        entity.status = PropertyStatus.EDIT_PENDING
    elif current_user.role in (UserRole.ADMIN, UserRole.APPROVER):
        action = Action.EDIT
        transition_from = entity.status
        transition_to = entity.status
        needs_approval = False
    else:
        raise ForbiddenError("Insufficient permissions")

    changed_fields = body.model_dump(exclude_none=True)

    if needs_approval:
        snapshot = {}
        for field in changed_fields:
            val = getattr(entity, field, None)
            if isinstance(val, Decimal):
                snapshot[field] = float(val)
            elif isinstance(val, uuid.UUID):
                snapshot[field] = str(val)  # type: ignore[assignment]
            elif isinstance(val, PyEnum):
                snapshot[field] = val.value
            else:
                snapshot[field] = val  # type: ignore[assignment]
    else:
        snapshot = None

    apply_to_entity(entity, body)

    if body.image_ids is not None:
        current_ids = await repo.get_file_ids_in_property(property_id)
        for fid in body.image_ids:
            if fid not in current_ids:
                await repo.create_image(property_id, fid, order=len(current_ids))

    entity = await repo.save(entity)

    transition = await repo.create_transition(
        property_id=property_id,
        from_status=transition_from,
        to_status=transition_to,
        action=action,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
    )

    if needs_approval:
        approval = ApprovalEntity(
            property_id=entity.id,
            transition_id=transition.id,
            transaction_type_id=entity.transaction_type_id,
            status=ApprovalStatus.PENDING,
            old_values=snapshot,
        )
        await approval_repo.save(approval)
        title = format_notification_title(
            event_type="listing_updated",
            transaction_type=entity.transaction_type.code if entity.transaction_type else None,
            actor_name=current_user.full_name,
            item_code=entity.code,
        )
        await notif_service.notify_admins_and_approvers(
            organization_id=current_user.organization_id,
            title=title,
            event_type="listing_updated",
            reference_type="property",
            reference_id=property_id,
            actor_name=current_user.full_name,
            transaction_type=entity.transaction_type.code if entity.transaction_type else None,
        )

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
