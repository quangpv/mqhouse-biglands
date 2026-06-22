import uuid

from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.shared.errors.exceptions import NotFoundError


async def delete_organization(
    org_id: uuid.UUID,
    repo: OrganizationRepo = Depends(OrganizationRepo),
) -> None:
    org = await repo.get(org_id)
    if org is None:
        raise NotFoundError("Organization not found")
    await repo.delete(org_id)
