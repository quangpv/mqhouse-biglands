import uuid

from fastapi import Depends, Path

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.mapper import entity_to_response
from src.modules.approvals.schemas import ApprovalResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError, NotFoundError


async def get_approval_detail(
    approval_id: uuid.UUID = Path(..., alias="approval_id"),
    repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ApprovalResponse:
    if current_user.role not in (UserRole.ADMIN, UserRole.APPROVER):
        raise ForbiddenError("Insufficient permissions")
    entity = await repo.get(approval_id)
    if not entity:
        raise NotFoundError("Approval not found")
    return entity_to_response(entity)
