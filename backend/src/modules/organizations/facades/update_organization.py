import uuid

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import organization_to_response
from src.modules.organizations.schemas import OrganizationResponse, UpdateOrganizationRequest
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def update_organization(
    org_id: uuid.UUID,
    data: UpdateOrganizationRequest,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    org = await repo.get(org_id)
    if org is None:
        raise NotFoundError("Organization not found")

    org.name = data.name
    org.display_name = data.display_name
    try:
        org = await repo.save(org)
    except IntegrityError:
        raise ConflictError("Organization name already exists")

    return organization_to_response(org)
