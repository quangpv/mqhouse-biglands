from fastapi import APIRouter, Depends, status

from src.data.entities.user import UserRole
from src.modules.organizations.facades.create_organization import (
    create_organization,
)
from src.modules.organizations.facades.delete_organization import (
    delete_organization,
)
from src.modules.organizations.facades.get_organization import (
    get_organization,
)
from src.modules.organizations.facades.list_organizations import (
    list_organizations,
)
from src.modules.organizations.facades.update_organization import (
    update_organization,
)
from src.modules.organizations.schemas import (
    OrganizationListResponse,
    OrganizationResponse,
)
from src.platform.auth import require_auth, require_role

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get(
    "/",
    response_model=OrganizationListResponse,
    dependencies=[Depends(require_auth)],
)
async def list_endpoint(result: OrganizationListResponse = Depends(list_organizations)):
    return result


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def create_endpoint(result: OrganizationResponse = Depends(create_organization)):
    return result


@router.get(
    "/{org_id}",
    response_model=OrganizationResponse,
    dependencies=[Depends(require_auth)],
)
async def get_endpoint(result: OrganizationResponse = Depends(get_organization)):
    return result


@router.put(
    "/{org_id}",
    response_model=OrganizationResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def update_endpoint(result: OrganizationResponse = Depends(update_organization)):
    return result


@router.delete(
    "/{org_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)
async def delete_endpoint(_: None = Depends(delete_organization)):
    return None
