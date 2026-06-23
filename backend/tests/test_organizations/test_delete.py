import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity

AGENT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000002")


@pytest.mark.asyncio
async def test_admin_can_delete_organization(client: AsyncClient, admin_token: str) -> None:
    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "to-delete",
            "display_name": "To Delete",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.delete(
        f"/organizations/{org_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_non_admin_cannot_delete_organization(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "delete-no-perm",
            "display_name": "No Perm",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.delete(
        f"/organizations/{org_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_nonexistent_organization_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.delete(
        f"/organizations/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_organization_without_auth_fails(client: AsyncClient) -> None:
    response = await client.delete(f"/organizations/{uuid.uuid4()}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_organization_with_active_users_returns_409(
    client: AsyncClient, admin_token: str, db_session: AsyncSession
) -> None:
    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "has-users",
            "display_name": "Has Users",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = uuid.UUID(create_resp.json()["id"])

    agent = await db_session.get(UserEntity, AGENT_UUID)
    agent.organization_id = org_id
    await db_session.commit()

    response = await client.delete(
        f"/organizations/{org_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
