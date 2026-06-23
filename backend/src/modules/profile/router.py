from fastapi import APIRouter, Depends, status

from src.modules.pins.facades.list_my_pins import list_my_pins
from src.modules.pins.schemas import MyPinListResponse
from src.modules.profile.facades.get_profile import get_profile
from src.modules.profile.schemas import ProfileResponse
from src.modules.properties.facades.list_my_properties import list_my_properties
from src.modules.properties.schemas import PropertyListResponse
from src.platform.auth import require_auth

router = APIRouter(tags=["profile"])


@router.get("/me", response_model=ProfileResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(require_auth)])
async def me(result: ProfileResponse = Depends(get_profile)):
    return result


@router.get("/me/pins", response_model=MyPinListResponse, dependencies=[Depends(require_auth)])
async def my_pins(result: MyPinListResponse = Depends(list_my_pins)):
    return result


@router.get("/me/properties", response_model=PropertyListResponse, dependencies=[Depends(require_auth)])
async def my_properties(result: PropertyListResponse = Depends(list_my_properties)):
    return result
