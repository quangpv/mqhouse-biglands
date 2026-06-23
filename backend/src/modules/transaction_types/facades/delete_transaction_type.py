import uuid

from fastapi import Depends

from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.shared.errors.exceptions import NotFoundError


async def delete_transaction_type(
    entity_id: uuid.UUID,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
) -> None:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Transaction type not found")
    await repo.delete(entity)
