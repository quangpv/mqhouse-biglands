from fastapi import APIRouter

from src.modules.approvals.facades.approve_approval import approve_approval
from src.modules.approvals.facades.get_approval_counts import get_approval_counts
from src.modules.approvals.facades.get_approval_detail import get_approval_detail
from src.modules.approvals.facades.list_approvals import list_approvals
from src.modules.approvals.facades.reject_approval import reject_approval

router = APIRouter(prefix="/approvals", tags=["Approvals"])

router.add_api_route("", endpoint=list_approvals, methods=["GET"])
router.add_api_route("/counts", endpoint=get_approval_counts, methods=["GET"])
router.add_api_route("/{approval_id}", endpoint=get_approval_detail, methods=["GET"])
router.add_api_route("/{approval_id}/approve", endpoint=approve_approval, methods=["POST"])
router.add_api_route("/{approval_id}/reject", endpoint=reject_approval, methods=["POST"])
