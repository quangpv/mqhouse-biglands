from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import entity_to_response, request_to_entity
from src.modules.organizations.schemas import (
    CreateOrganizationRequest,
    OrganizationResponse,
)
from src.shared.errors.exceptions import ConflictError


async def create_organization(
    body: CreateOrganizationRequest,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    existing = await repo.get_by_name(body.name)
    if existing:
        raise ConflictError(f"Organization with name '{body.name}' already exists")

    entity = request_to_entity(body)
    entity = await repo.save(entity)

    return entity_to_response(entity)
