import uuid

from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import apply_to_entity, entity_to_response
from src.modules.organizations.schemas import (
    OrganizationResponse,
    UpdateOrganizationRequest,
)
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def update_organization(
    org_id: uuid.UUID,
    body: UpdateOrganizationRequest,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationResponse:
    entity = await repo.get(org_id)
    if entity is None:
        raise NotFoundError("Organization not found")

    if body.name != entity.name:
        existing = await repo.get_by_name(body.name)
        if existing:
            raise ConflictError(f"Organization with name '{body.name}' already exists")

    entity = apply_to_entity(entity, body)
    await repo.save(entity)

    return entity_to_response(entity)
