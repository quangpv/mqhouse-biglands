import uuid

from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import organization_to_response
from src.modules.organizations.schemas import OrganizationListResponse, OrganizationResponse
from src.shared.errors.exceptions import NotFoundError
from src.shared.pagination import build_paginated_response


async def list_organizations(
    page: int = 1,
    size: int = 20,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationListResponse:
    all_orgs = await repo.list_all()
    total = len(all_orgs)
    start = (page - 1) * size
    end = start + size
    page_items = all_orgs[start:end]
    items = [organization_to_response(org) for org in page_items]
    return OrganizationListResponse(
        **build_paginated_response(items, page, size, total).model_dump(),
    )


async def get_organization(
    org_id: uuid.UUID,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    org = await repo.get(org_id)
    if org is None:
        raise NotFoundError("Organization not found")
    return organization_to_response(org)
