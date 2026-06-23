from fastapi import APIRouter, Depends, status

from src.data.entities.user import UserRole
from src.modules.transaction_types.facades.create_transaction_type import (
    create_transaction_type,
)
from src.modules.transaction_types.facades.delete_transaction_type import (
    delete_transaction_type,
)
from src.modules.transaction_types.facades.get_transaction_type import (
    get_transaction_type,
)
from src.modules.transaction_types.facades.list_transaction_types import (
    list_transaction_types,
)
from src.modules.transaction_types.facades.update_transaction_type import (
    update_transaction_type,
)
from src.modules.transaction_types.schemas import (
    TransactionTypeListResponse,
    TransactionTypeResponse,
)
from src.platform.auth import require_auth, require_role

router = APIRouter(prefix="/transaction-types", tags=["transaction-types"])


@router.get(
    "/",
    response_model=TransactionTypeListResponse,
    dependencies=[Depends(require_auth)],
)
async def list_endpoint(result: TransactionTypeListResponse = Depends(list_transaction_types)):
    return result


@router.post(
    "/",
    response_model=TransactionTypeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def create_endpoint(result: TransactionTypeResponse = Depends(create_transaction_type)):
    return result


@router.get(
    "/{entity_id}",
    response_model=TransactionTypeResponse,
    dependencies=[Depends(require_auth)],
)
async def get_endpoint(result: TransactionTypeResponse = Depends(get_transaction_type)):
    return result


@router.put(
    "/{entity_id}",
    response_model=TransactionTypeResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def update_endpoint(result: TransactionTypeResponse = Depends(update_transaction_type)):
    return result


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def delete_endpoint(_: None = Depends(delete_transaction_type)):
    return None
