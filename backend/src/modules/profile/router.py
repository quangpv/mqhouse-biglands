from fastapi import APIRouter, Depends, status

from src.modules.profile.facades.get_profile import get_profile
from src.modules.profile.schemas import ProfileResponse
from src.platform.auth import require_auth

router = APIRouter(tags=["profile"])


@router.get("/me", response_model=ProfileResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(require_auth)])
async def me(result: ProfileResponse = Depends(get_profile)):
    return result
