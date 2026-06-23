import uuid

from fastapi import Depends, Path

from src.data.entities.approval import ApprovalStatus
from src.data.entities.property import Action, PropertyStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.data.repositories.property_repo import PropertyRepo
from src.modules.approvals.mapper import entity_to_response
from src.modules.approvals.schemas import ApprovalDecisionRequest, ApprovalResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ConflictError, ForbiddenError, NotFoundError
from src.shared.services.notification_service import NotificationService
from src.shared.utils.notification_formatter import format_notification_title

_REJECT_MAP: dict[PropertyStatus, PropertyStatus] = {
    PropertyStatus.POST_PENDING: PropertyStatus.DRAFT,
    PropertyStatus.DEPOSIT_PENDING: PropertyStatus.AVAILABLE,
    PropertyStatus.CANCEL_PENDING: PropertyStatus.DEPOSITED,
    PropertyStatus.COMPLETE_PENDING: PropertyStatus.DEPOSITED,
}


_REJECT_EVENT_MAP: dict[PropertyStatus, str] = {
    PropertyStatus.POST_PENDING: "listing_post_rejected",
    PropertyStatus.DEPOSIT_PENDING: "deposit_rejected",
    PropertyStatus.SOLDOUT_PENDING: "sold_out_rejected",
    PropertyStatus.CANCEL_PENDING: "cancellation_rejected",
    PropertyStatus.COMPLETE_PENDING: "closure_rejected",
}


async def reject_approval(
    body: ApprovalDecisionRequest,
    approval_id: uuid.UUID = Path(..., alias="approval_id"),
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    property_repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
    notif_service: NotificationService = Depends(NotificationService),
) -> ApprovalResponse:
    approval = await approval_repo.get(approval_id)
    if not approval:
        raise NotFoundError("Approval not found")

    if approval.status != ApprovalStatus.PENDING:
        raise ConflictError("Approval is not in pending status")

    if current_user.role not in (UserRole.ADMIN, UserRole.APPROVER):
        raise ForbiddenError("Insufficient permissions")

    prop = approval.property
    original_status = prop.status

    if original_status == PropertyStatus.EDIT_PENDING:
        to_status = (approval.transition.from_status if approval.transition else None) or PropertyStatus.DRAFT
    elif original_status == PropertyStatus.SOLDOUT_PENDING:
        to_status = (approval.transition.from_status if approval.transition else None) or PropertyStatus.AVAILABLE
    else:
        mapped = _REJECT_MAP.get(prop.status)
        if mapped is None:
            raise ConflictError(f"Cannot reject property in status {prop.status.value}")
        to_status = mapped

    t2 = await property_repo.create_transition(
        property_id=prop.id,
        from_status=prop.status,
        to_status=to_status,
        action=Action.REJECT,
        actor_id=current_user.id,
        actor_name=current_user.full_name,
        notes=body.reason,
    )

    prop.status = to_status
    await property_repo.save(prop)

    approval.status = ApprovalStatus.REJECTED
    approval.decision_transition_id = t2.id
    approval = await approval_repo.save(approval)

    owner_id = prop.created_by_id
    if owner_id:
        event_type = _REJECT_EVENT_MAP.get(original_status)
        if event_type is None and original_status == PropertyStatus.EDIT_PENDING:
            event_type = "edit_rejected"
        if event_type is not None:
            title = format_notification_title(
                event_type=event_type,
                transaction_type=prop.transaction_type.code if prop.transaction_type else None,
                actor_name=current_user.full_name,
                item_code=prop.code,
            )
            await notif_service.notify_property_owner(
                owner_id=owner_id,
                title=title,
                event_type=event_type,
                reference_type="property",
                reference_id=prop.id,
                actor_name=current_user.full_name,
                transaction_type=prop.transaction_type.code if prop.transaction_type else None,
            )

    return entity_to_response(approval)
