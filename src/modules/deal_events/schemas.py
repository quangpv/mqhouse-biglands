import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ReportDepositRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=255)
    customer_phone: str | None = Field(None, max_length=20)
    deposit_amount: Decimal = Field(..., gt=0)
    notes: str | None = None


class ReportClosureRequest(BaseModel):
    notes: str | None = None


class ReportCancellationRequest(BaseModel):
    notes: str = Field(..., min_length=1)


class ReportSoldOutRequest(BaseModel):
    notes: str | None = None


class DealEventResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    event_type: str
    reported_by_id: uuid.UUID
    confirmed_by_id: uuid.UUID | None = None
    confirmed_at: datetime | None = None
    notes: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    deposit_amount: Decimal | None = None
    created_at: datetime
