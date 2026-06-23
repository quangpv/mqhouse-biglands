from fastapi import Depends

from src.data.entities.approval import ApprovalStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.schemas import ApprovalCountItem
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError


async def get_approval_counts(
    repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> list[ApprovalCountItem]:
    if current_user.role not in (UserRole.ADMIN, UserRole.APPROVER):
        raise ForbiddenError("Insufficient permissions")
    results = await repo.count_by_transaction_type(status=ApprovalStatus.PENDING)
    return [
        ApprovalCountItem(transaction_type_code=code, count=count)
        for code, count in results
    ]
