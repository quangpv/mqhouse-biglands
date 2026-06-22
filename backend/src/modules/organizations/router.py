from fastapi import APIRouter, Depends, status

from src.modules.organizations.facades.create_organization import create_organization
from src.modules.organizations.facades.delete_organization import delete_organization
from src.modules.organizations.facades.list_organizations import get_organization, list_organizations
from src.modules.organizations.facades.update_organization import update_organization
from src.modules.organizations.schemas import OrganizationListResponse, OrganizationResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("", response_model=OrganizationListResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def list_all(result: OrganizationListResponse = Depends(list_organizations)):
    return result


@router.get("/{org_id}", response_model=OrganizationResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def get(result: OrganizationResponse = Depends(get_organization)):
    return result


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("ADMIN"))])
async def create(result: OrganizationResponse = Depends(create_organization)):
    return result


@router.put("/{org_id}", response_model=OrganizationResponse, dependencies=[Depends(require_role("ADMIN"))])
async def update(result: OrganizationResponse = Depends(update_organization)):
    return result


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("ADMIN"))])
async def delete(result = Depends(delete_organization)):
    return result
