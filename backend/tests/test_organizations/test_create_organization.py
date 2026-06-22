import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateOrganization:
    NEW_ORG = {
        "name": "test-org",
        "display_name": "Test Organization",
    }

    async def test_admin_can_create_organization(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/organizations",
            json=self.NEW_ORG,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test-org"
        assert data["display_name"] == "Test Organization"

    async def test_agent_cannot_create_organization(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            "/organizations",
            json=self.NEW_ORG,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_create_organization_without_name_returns_400(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/organizations",
            json={"display_name": "No Name"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 422

    async def test_create_duplicate_organization_name_returns_409(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        await client.post(
            "/organizations",
            json={"name": "dup-org", "display_name": "Dup"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        response = await client.post(
            "/organizations",
            json={"name": "dup-org", "display_name": "Dup Again"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409
