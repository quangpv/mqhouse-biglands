from fastapi import APIRouter, Depends, status

from src.modules.auth.facades.change_password import change_password
from src.modules.auth.facades.forgot_password import forgot_password
from src.modules.auth.facades.get_current_user import get_current_user_facade
from src.modules.auth.facades.login import login
from src.modules.auth.facades.logout import logout
from src.modules.auth.facades.refresh import refresh
from src.modules.auth.facades.reset_password import reset_password
from src.modules.auth.schemas import (
    ChangePasswordResponse,
    ForgotPasswordResponse,
    LoginResponse,
    LogoutResponse,
    RefreshTokenResponse,
    ResetPasswordResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_endpoint(result: LoginResponse = Depends(login)):
    return result


@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
async def refresh_endpoint(result: RefreshTokenResponse = Depends(refresh)):
    return result


@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout_endpoint(result: LogoutResponse = Depends(logout)):
    return result


@router.post("/change-password", response_model=ChangePasswordResponse, status_code=status.HTTP_200_OK)
async def change_password_endpoint(result: ChangePasswordResponse = Depends(change_password)):
    return result


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me_endpoint(result: UserResponse = Depends(get_current_user_facade)):
    return result


@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
async def forgot_password_endpoint(result: ForgotPasswordResponse = Depends(forgot_password)):
    return result


@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_password_endpoint(result: ResetPasswordResponse = Depends(reset_password)):
    return result
