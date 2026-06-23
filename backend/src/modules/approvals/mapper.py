import uuid

from src.modules.approvals.schemas import (
    ApprovalRequestDetail,
    ApprovalResponse,
    CreatorInfo,
    DecisionInfo,
)
from src.modules.properties.mapper import entity_to_response as property_to_response


def entity_to_response(entity) -> ApprovalResponse:
    prop_resp = property_to_response(entity.property)

    t1 = entity.transition
    request = ApprovalRequestDetail(
        action=t1.action.value if t1 and t1.action else "",
        from_status=t1.from_status.value if t1 and t1.from_status else None,
        to_status=t1.to_status.value if t1 and t1.to_status else "",
        notes=t1.notes if t1 else None,
        customer_name=t1.customer_name if t1 else None,
        customer_phone=t1.customer_phone if t1 else None,
        contract_date=t1.contract_date if t1 else None,
        file_ids=[tf.file_id for tf in (t1.files or [])] if t1 else [],
        old_values=entity.old_values,
    )

    decision = None
    t2 = entity.decision_transition
    if t2:
        decision = DecisionInfo(
            decided_by=CreatorInfo(
                id=t2.actor_id,
                full_name=t2.actor_name,
                phone=None,
            ),
            reason=t2.notes,
            decided_at=t2.created_at,
        )

    requested_by = CreatorInfo(id=uuid.uuid4(), full_name="", phone=None)
    if t1:
        requested_by = CreatorInfo(
            id=t1.actor_id,
            full_name=t1.actor_name,
            phone=None,
        )

    tt_code = entity.transaction_type.code if entity.transaction_type else ""

    return ApprovalResponse(
        id=entity.id,
        property=prop_resp,
        transaction_type=tt_code,
        status=entity.status,
        requested_by=requested_by,
        request=request,
        decision=decision,
        created_at=entity.created_at,
    )
