from fastapi import Depends

from src.data.entities.transaction_type import TransactionTypeEntity
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.modules.transaction_types.mapper import entity_to_response
from src.modules.transaction_types.schemas import (
    CreateTransactionTypeRequest,
    TransactionTypeResponse,
)
from src.platform.auth import get_current_user, require_role
from src.shared.errors.exceptions import ConflictError


async def create_transaction_type(
    body: CreateTransactionTypeRequest,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
    current_user: UserEntity = Depends(require_role(UserRole.ADMIN.value)),
) -> TransactionTypeResponse:
    existing = await repo.get_by_code(body.code)
    if existing:
        raise ConflictError(f"Transaction type with code '{body.code}' already exists")

    entity = TransactionTypeEntity(code=body.code, display_name=body.display_name)
    entity = await repo.save(entity)
    return entity_to_response(entity)
