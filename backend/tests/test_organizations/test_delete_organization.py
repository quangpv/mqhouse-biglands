import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestDeleteOrganization:
    async def test_admin_can_delete_organization(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        create_resp = await client.post(
            "/organizations",
            json={"name": "temp-org", "display_name": "Temp Org"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == 201
        org_id = create_resp.json()["id"]

        response = await client.delete(
            f"/organizations/{org_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    async def test_agent_cannot_delete_organization(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.delete(
            "/organizations/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_delete_nonexistent_organization_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.delete(
            "/organizations/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
