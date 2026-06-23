from fastapi import APIRouter, Depends, status

from src.data.entities.user import UserRole
from src.modules.users.facades.create_user import create_user
from src.modules.users.facades.deactivate_user import deactivate_user
from src.modules.users.facades.get_user import get_user
from src.modules.users.facades.list_users import list_users
from src.modules.users.facades.reactivate_user import reactivate_user
from src.modules.users.facades.update_user import update_user
from src.modules.users.schemas import UserListData, UserResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def create_endpoint(result: UserResponse = Depends(create_user)):
    return result


@router.get(
    "/",
    response_model=UserListData,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def list_endpoint(result: UserListData = Depends(list_users)):
    return result


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def get_endpoint(result: UserResponse = Depends(get_user)):
    return result


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def update_endpoint(result: UserResponse = Depends(update_user)):
    return result


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def deactivate_endpoint(result: UserResponse = Depends(deactivate_user)):
    return result


@router.patch(
    "/{user_id}/reactivate",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def reactivate_endpoint(result: UserResponse = Depends(reactivate_user)):
    return result
