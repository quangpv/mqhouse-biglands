from fastapi import Depends, Query

from src.data.entities.approval import ApprovalStatus
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.mapper import entity_to_response
from src.modules.approvals.schemas import ApprovalListResponse, PageDTO
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import ForbiddenError


async def list_approvals(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: ApprovalStatus | None = Query(None),
    transaction_type_ids: list[str] = Query([]),
    search: str | None = Query(None),
    district: list[str] = Query([]),
    ward: list[str] = Query([]),
    price_from: float | None = Query(None),
    price_to: float | None = Query(None),
    area_from: float | None = Query(None),
    area_to: float | None = Query(None),
    requested_by_id: str | None = Query(None),
    repo: ApprovalRepo = Depends(ApprovalRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> ApprovalListResponse:
    if current_user.role not in (UserRole.ADMIN, UserRole.APPROVER):
        raise ForbiddenError("Insufficient permissions")
    import uuid
    from decimal import Decimal

    tt_ids = [uuid.UUID(t) for t in transaction_type_ids] if transaction_type_ids else None
    r_id = uuid.UUID(requested_by_id) if requested_by_id else None

    rows, total = await repo.search(
        page=page,
        size=size,
        status=status,
        transaction_type_ids=tt_ids,
        search=search,
        districts=district if district else None,
        wards=ward if ward else None,
        price_from=Decimal(str(price_from)) if price_from is not None else None,
        price_to=Decimal(str(price_to)) if price_to is not None else None,
        area_from=Decimal(str(area_from)) if area_from is not None else None,
        area_to=Decimal(str(area_to)) if area_to is not None else None,
        requested_by_id=r_id,
    )

    total_pages = (total + size - 1) // size if total > 0 else 0

    return ApprovalListResponse(
        data=[entity_to_response(row) for row in rows],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
