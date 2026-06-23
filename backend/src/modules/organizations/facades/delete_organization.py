import uuid

from fastapi import Depends

from src.data.repositories.organization_repo import OrganizationRepo
from src.data.repositories.user_repo import UserRepo
from src.shared.errors.exceptions import ConflictError, NotFoundError


async def delete_organization(
    org_id: uuid.UUID,
    repo: OrganizationRepo = Depends(OrganizationRepo),
    user_repo: UserRepo = Depends(UserRepo),
) -> None:
    entity = await repo.get(org_id)
    if entity is None:
        raise NotFoundError("Organization not found")

    users = await user_repo.get_by_organization(org_id)
    if users:
        raise ConflictError("Cannot delete organization with active users")

    await repo.delete(entity)
