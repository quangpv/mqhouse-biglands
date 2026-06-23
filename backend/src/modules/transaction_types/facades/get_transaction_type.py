import uuid

from fastapi import Depends

from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import TransactionTypeResponse
from src.shared.errors.exceptions import NotFoundError


async def get_transaction_type(
    entity_id: uuid.UUID,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
) -> TransactionTypeResponse:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Transaction type not found")
    return entity_to_response(entity)
