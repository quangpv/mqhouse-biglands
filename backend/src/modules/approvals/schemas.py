import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from src.data.entities.approval import ApprovalStatus
from src.modules.properties.schemas import CreatorInfo, PageDTO, PropertyResponse


class ApprovalRequestDetail(BaseModel):
    action: str
    from_status: str | None = None
    to_status: str
    notes: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    contract_date: date | None = None
    file_ids: list[uuid.UUID] = []
    old_values: dict[str, Any] | None = None


class DecisionInfo(BaseModel):
    decided_by: CreatorInfo
    reason: str | None = None
    decided_at: datetime


class ApprovalResponse(BaseModel):
    id: uuid.UUID
    property: PropertyResponse
    transaction_type: str
    status: ApprovalStatus
    requested_by: CreatorInfo
    request: ApprovalRequestDetail
    decision: DecisionInfo | None = None
    created_at: datetime


class ApprovalListResponse(BaseModel):
    data: list[ApprovalResponse]
    metadata: PageDTO


class ApprovalCountItem(BaseModel):
    transaction_type_code: str
    count: int


class ApprovalDecisionRequest(BaseModel):
    reason: str | None = None
