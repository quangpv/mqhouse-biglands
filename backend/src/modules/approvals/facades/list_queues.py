from fastapi import Depends

from src.data.entities.approval import ApprovalType
from src.data.repositories.approval_repo import ApprovalRepo
from src.modules.approvals.schemas import QueueCountResponse, QueueListResponse


async def list_queues(
    repo: ApprovalRepo = Depends(ApprovalRepo),
) -> QueueListResponse:
    counts = await repo.get_queue_counts()
    queues = [
        QueueCountResponse(
            approval_type=str(approval_type.value),
            transaction_type=str(transaction_type.value),
            count=count,
        )
        for approval_type, transaction_type, count in counts
    ]

    all_approval_types = ["LISTING_POST", "DEPOSIT", "CLOSURE", "CANCELLATION", "SOLD_OUT"]
    all_transaction_types = ["SANG_NHUONG", "CHO_THUE", "BAN"]

    seen = {(q.approval_type, q.transaction_type) for q in queues}
    for at in all_approval_types:
        for tt in all_transaction_types:
            if (at, tt) not in seen:
                queues.append(QueueCountResponse(approval_type=at, transaction_type=tt, count=0))

    queues.sort(key=lambda q: (ALL_TYPES_ORDER.index(q.approval_type), ALL_TRANS_ORDER.index(q.transaction_type)))

    return QueueListResponse(queues=queues)


ALL_TYPES_ORDER = ["LISTING_POST", "DEPOSIT", "CLOSURE", "CANCELLATION", "SOLD_OUT"]
ALL_TRANS_ORDER = ["SANG_NHUONG", "CHO_THUE", "BAN"]
