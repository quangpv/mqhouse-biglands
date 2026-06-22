from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.data.entities.organization import OrganizationEntity
from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import organization_to_response
from src.modules.organizations.schemas import CreateOrganizationRequest, OrganizationResponse
from src.shared.errors.exceptions import ConflictError


async def create_organization(
    data: CreateOrganizationRequest,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    org = OrganizationEntity(
        name=data.name,
        display_name=data.display_name,
    )
    try:
        org = await repo.create(org)
    except IntegrityError:
        raise ConflictError("Organization name already exists")

    return organization_to_response(org)
