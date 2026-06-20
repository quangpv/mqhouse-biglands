
from fastapi import APIRouter, Depends, status

from src.modules.users.facades.assign_role import assign_role
from src.modules.users.facades.create_user import create_user
from src.modules.users.facades.deactivate_user import deactivate_user
from src.modules.users.facades.get_user import get_user
from src.modules.users.facades.list_users import list_users
from src.modules.users.facades.reactivate_user import reactivate_user
from src.modules.users.facades.update_user import update_user
from src.modules.users.schemas import UserListResponse, UserResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_role("ADMIN"))])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(result: UserResponse = Depends(create_user)):
    return result


@router.get("", response_model=UserListResponse)
async def list_all(result: UserListResponse = Depends(list_users)):
    return result


@router.get("/{user_id}", response_model=UserResponse)
async def get(result: UserResponse = Depends(get_user)):
    return result


@router.put("/{user_id}", response_model=UserResponse)
async def update(result: UserResponse = Depends(update_user)):
    return result


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate(result: UserResponse = Depends(deactivate_user)):
    return result


@router.patch("/{user_id}/reactivate", response_model=UserResponse)
async def reactivate(result: UserResponse = Depends(reactivate_user)):
    return result


@router.patch("/{user_id}/role", response_model=UserResponse)
async def assign(result: UserResponse = Depends(assign_role)):
    return result
