from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.modules.organizations.mapper import entity_to_response
from src.modules.organizations.schemas import OrganizationListResponse


async def list_organizations(
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> OrganizationListResponse:
    entities = await repo.get_all()
    return [entity_to_response(entity) for entity in entities]
