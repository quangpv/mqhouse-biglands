from fastapi import Depends

from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import TransactionTypeListResponse


async def list_transaction_types(
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
) -> TransactionTypeListResponse:
    entities = await repo.get_all()
    return [entity_to_response(e) for e in entities]
