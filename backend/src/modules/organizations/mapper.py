from src.data.entities.organization import OrganizationEntity
from src.modules.organizations.schemas import OrganizationResponse


def organization_to_response(entity: OrganizationEntity) -> OrganizationResponse:
    return OrganizationResponse(
        id=entity.id,
        name=entity.name,
        display_name=entity.display_name,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
