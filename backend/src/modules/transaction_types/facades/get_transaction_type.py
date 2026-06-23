import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import TransactionTypeResponse
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def get_transaction_type(
    entity_id: uuid.UUID,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> TransactionTypeResponse:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Transaction type not found")
    return entity_to_response(entity)
