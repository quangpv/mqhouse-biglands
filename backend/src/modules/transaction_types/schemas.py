import uuid
from datetime import datetime

from pydantic import BaseModel


class TransactionTypeInfo(BaseModel):
    id: uuid.UUID
    code: str
    display_name: str
    created_at: datetime
    updated_at: datetime


class TransactionTypeResponse(TransactionTypeInfo):
    pass


class CreateTransactionTypeRequest(BaseModel):
    code: str
    display_name: str


class UpdateTransactionTypeRequest(BaseModel):
    code: str
    display_name: str


TransactionTypeListResponse = list[TransactionTypeInfo]
