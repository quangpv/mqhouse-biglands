import uuid

from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import entity_to_response
from src.modules.organizations.schemas import OrganizationResponse
from src.shared.errors.exceptions import NotFoundError


async def get_organization(
    org_id: uuid.UUID,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    entity = await repo.get(org_id)
    if entity is None:
        raise NotFoundError("Organization not found")

    return entity_to_response(entity)
