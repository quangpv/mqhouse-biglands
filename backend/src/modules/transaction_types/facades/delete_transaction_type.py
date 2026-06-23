import uuid

from fastapi import Depends

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.transaction_type_repo import TransactionTypeRepo
from src.platform.auth import require_role
from src.shared.errors.exceptions import NotFoundError


async def delete_transaction_type(
    entity_id: uuid.UUID,
    repo: TransactionTypeRepo = Depends(TransactionTypeRepo),
    current_user: UserEntity = Depends(require_role(UserRole.ADMIN.value)),
) -> None:
    entity = await repo.get(entity_id)
    if entity is None:
        raise NotFoundError("Transaction type not found")
    await repo.delete(entity)
