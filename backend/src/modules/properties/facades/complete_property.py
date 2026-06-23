import uuid

from fastapi import Depends, Path

from src.data.entities.approval import ApprovalEntity, ApprovalStatus
from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import CompleteRequest, PropertyResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError
from src.shared.services.notification_service import NotificationService
from src.shared.utils.notification_formatter import format_notification_title


async def complete_property(
    body: CompleteRequest,
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
    notif_service: NotificationService = Depends(NotificationService),
) -> PropertyResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    if entity.status != PropertyStatus.DEPOSITED:
        raise ForbiddenError("Only deposited properties can be completed")

    from datetime import date
    if body.contract_date < date.today():
        raise ForbiddenError("Contract date must be today or later")

    if len(body.file_ids) > 10:
        raise ForbiddenError("Maximum 10 files allowed")

    if current_user.role == UserRole.SALE:
        new_status = PropertyStatus.COMPLETE_PENDING
    elif current_user.role in (UserRole.ADMIN, UserRole.APPROVER):
        new_status = PropertyStatus.COMPLETED
    else:
        raise ForbiddenError("Insufficient permissions")

    old_status = entity.status
    entity.status = new_status
    entity = await repo.save(entity)

    transition = await repo.create_transition(
        property_id=property_id,
        from_status=old_status,
        to_status=new_status,
        action=Action.COMPLETE,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
        notes=body.notes,
        customer_name=body.customer_name,
        customer_phone=body.customer_phone,
        contract_date=body.contract_date,
        file_ids=body.file_ids or None,
    )

    if current_user.role == UserRole.SALE:
        approval = ApprovalEntity(
            property_id=entity.id,
            transition_id=transition.id,
            transaction_type_id=entity.transaction_type_id,
            status=ApprovalStatus.PENDING,
        )
        await approval_repo.save(approval)
        title = format_notification_title(
            event_type="closure_reported",
            transaction_type=entity.transaction_type.code if entity.transaction_type else None,
            actor_name=current_user.full_name,
            item_code=entity.code,
        )
        await notif_service.notify_admins_and_approvers(
            organization_id=current_user.organization_id,
            title=title,
            event_type="closure_reported",
            reference_type="property",
            reference_id=property_id,
            actor_name=current_user.full_name,
            transaction_type=entity.transaction_type.code if entity.transaction_type else None,
        )

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    return entity_to_response(reloaded)
