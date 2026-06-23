from fastapi import APIRouter, Depends, status

from src.data.entities.user import UserRole
from src.modules.property_types.facades.create_property_type import (
    create_property_type,
)
from src.modules.property_types.facades.delete_property_type import (
    delete_property_type,
)
from src.modules.property_types.facades.get_property_type import (
    get_property_type,
)
from src.modules.property_types.facades.list_property_types import (
    list_property_types,
)
from src.modules.property_types.facades.update_property_type import (
    update_property_type,
)
from src.modules.property_types.schemas import (
    PropertyTypeListResponse,
    PropertyTypeResponse,
)
from src.platform.auth import require_auth, require_role

router = APIRouter(prefix="/property-types", tags=["property-types"])


@router.get(
    "/",
    response_model=PropertyTypeListResponse,
    dependencies=[Depends(require_auth)],
)
async def list_endpoint(result: PropertyTypeListResponse = Depends(list_property_types)):
    return result


@router.post(
    "/",
    response_model=PropertyTypeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def create_endpoint(result: PropertyTypeResponse = Depends(create_property_type)):
    return result


@router.get(
    "/{entity_id}",
    response_model=PropertyTypeResponse,
    dependencies=[Depends(require_auth)],
)
async def get_endpoint(result: PropertyTypeResponse = Depends(get_property_type)):
    return result


@router.put(
    "/{entity_id}",
    response_model=PropertyTypeResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def update_endpoint(result: PropertyTypeResponse = Depends(update_property_type)):
    return result


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def delete_endpoint(_: None = Depends(delete_property_type)):
    return None
