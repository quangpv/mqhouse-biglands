from fastapi import APIRouter, Depends, status

from src.modules.hots.facades.list_hot_properties import list_hot_properties
from src.modules.hots.facades.promote_to_hot import promote_to_hot
from src.modules.hots.facades.remove_from_hot import remove_from_hot
from src.modules.hots.schemas import HotPropertyListResponse, HotPropertyResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/properties", tags=["hots"])


@router.get("/hots", response_model=HotPropertyListResponse)
async def list_hots_endpoint(result: HotPropertyListResponse = Depends(list_hot_properties)):
    return result


@router.post(
    "/{property_id}/hots",
    response_model=HotPropertyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("ADMIN"))],
)
async def promote_endpoint(result: HotPropertyResponse = Depends(promote_to_hot)):
    return result


@router.delete(
    "/{property_id}/hots",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("ADMIN"))],
)
async def remove_endpoint(result: None = Depends(remove_from_hot)):
    return result
