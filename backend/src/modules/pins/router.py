from fastapi import APIRouter, Depends, status

from src.modules.pins.facades.add_pin import add_pin
from src.modules.pins.facades.remove_pin import remove_pin
from src.modules.pins.schemas import PinResponse
from src.platform.auth import require_auth

router = APIRouter(prefix="/properties/{property_id}/pins", tags=["pins"])


@router.post("", response_model=PinResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_auth)])
async def add_pin_endpoint(result: PinResponse = Depends(add_pin)):
    return result


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_auth)])
async def remove_pin_endpoint(result: None = Depends(remove_pin)):
    return result
