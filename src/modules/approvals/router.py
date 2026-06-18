from fastapi import APIRouter, Depends, status

from src.modules.approvals.facades.approve_item import approve_item
from src.modules.approvals.facades.bulk_approve import bulk_approve
from src.modules.approvals.facades.get_approval import get_approval
from src.modules.approvals.facades.list_queue_items import list_queue_items
from src.modules.approvals.facades.list_queues import list_queues
from src.modules.approvals.facades.reject_item import reject_item
from src.modules.approvals.schemas import ApprovalDetailResponse, ApproveResponse, BulkApproveResponse, QueueItemListResponse, QueueListResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("/queues", response_model=QueueListResponse, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def queues(result: QueueListResponse = Depends(list_queues)):
    return result


@router.get("/queues/{queue_type}", response_model=QueueItemListResponse, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def queue_items(result: QueueItemListResponse = Depends(list_queue_items)):
    return result


@router.get("/{listing_id}", response_model=ApprovalDetailResponse, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def detail(result: ApprovalDetailResponse = Depends(get_approval)):
    return result


@router.post("/{listing_id}/approve", response_model=ApproveResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def approve(result: ApproveResponse = Depends(approve_item)):
    return result


@router.post("/{listing_id}/reject", response_model=ApproveResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def reject(result: ApproveResponse = Depends(reject_item)):
    return result


@router.post("/bulk-approve", response_model=BulkApproveResponse, dependencies=[Depends(require_role("APPROVER", "ADMIN"))])
async def bulk(result: BulkApproveResponse = Depends(bulk_approve)):
    return result
