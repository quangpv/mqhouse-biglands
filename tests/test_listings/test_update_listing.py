import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestUpdateListing:
    async def test_owner_can_update_non_critical_fields_without_status_change(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_con_hang}",
            json={"description": "Updated description"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
        assert data["status"] == "CON_HANG"

    async def test_updating_price_on_CON_HANG_triggers_re_approval(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_con_hang}",
            json={"price": "9999999999"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "PENDING_APPROVAL"

    async def test_updating_area_width_on_CON_HANG_triggers_re_approval(
        self, client: AsyncClient, admin_token: str, admin_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{admin_con_hang}",
            json={"area_width": "10.0"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "PENDING_APPROVAL"

    async def test_non_owner_cannot_update_listing(
        self, client: AsyncClient, agent_token: str, admin_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{admin_con_hang}",
            json={"description": "Hacked"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_update_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            "/listings/00000000-0000-0000-0000-000000000099",
            json={"description": "Not found"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_update_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.put(
            "/listings/00000000-0000-0000-0000-000000000099",
            json={"description": "No auth"},
        )
        assert response.status_code == 401
