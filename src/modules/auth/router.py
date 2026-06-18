from fastapi import APIRouter, Depends, status

from src.modules.auth.facades.get_current_user import get_current_user_facade
from src.modules.auth.facades.login import login
from src.modules.auth.facades.logout import logout
from src.modules.auth.schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_endpoint(result: LoginResponse = Depends(login)):
    return result


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endpoint(result = Depends(logout)):
    return result


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me_endpoint(result: UserResponse = Depends(get_current_user_facade)):
    return result
