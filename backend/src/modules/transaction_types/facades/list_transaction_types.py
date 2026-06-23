from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import TransactionTypeListResponse
from src.platform.auth import get_current_user


async def list_transaction_types(
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> TransactionTypeListResponse:
    entities = await repo.get_all()
    return [entity_to_response(e) for e in entities]
