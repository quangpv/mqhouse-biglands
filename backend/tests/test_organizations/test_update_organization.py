import pytest
from httpx import AsyncClient

from tests.test_organizations.conftest import ORG_MQ_LAND_ID

pytestmark = pytest.mark.asyncio


class TestUpdateOrganization:
    async def test_admin_can_update_organization(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            f"/organizations/{ORG_MQ_LAND_ID}",
            json={"name": "mq-land-v2", "display_name": "MQ Land V2"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "mq-land-v2"
        assert data["display_name"] == "MQ Land V2"

    async def test_agent_cannot_update_organization(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.put(
            f"/organizations/{ORG_MQ_LAND_ID}",
            json={"name": "hacked", "display_name": "Hacked"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_update_nonexistent_organization_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            "/organizations/00000000-0000-0000-0000-000000009999",
            json={"name": "ghost", "display_name": "Ghost"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
