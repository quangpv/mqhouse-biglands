import pytest
from httpx import AsyncClient

from tests.test_organizations.conftest import ORG_MQ_LAND_ID

pytestmark = pytest.mark.asyncio


class TestGetOrganization:
    async def test_admin_can_get_organization_by_id(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/organizations/{ORG_MQ_LAND_ID}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(ORG_MQ_LAND_ID)
        assert data["name"] == "mq-land"
        assert data["display_name"] == "MQ Land"

    async def test_get_nonexistent_organization_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/organizations/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_get_organization(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get(f"/organizations/{ORG_MQ_LAND_ID}")
        assert response.status_code == 401
