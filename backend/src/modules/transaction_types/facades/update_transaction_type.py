import uuid

from fastapi import Depends

from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import (
    TransactionTypeResponse,
    UpdateTransactionTypeRequest,
)
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def update_transaction_type(
    entity_id: uuid.UUID,
    body: UpdateTransactionTypeRequest,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
) -> TransactionTypeResponse:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Transaction type not found")

    if body.code != entity.code:
        existing = await repo.get_by_code(body.code)
        if existing:
            raise ConflictError(f"Transaction type with code '{body.code}' already exists")

    entity.code = body.code
    entity.display_name = body.display_name
    await repo.save(entity)
    return entity_to_response(entity)
