import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestReportSoldOut:
    async def test_agent_reports_sold_out_on_con_hang_listing(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/sold-out",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "SOLD_OUT_REPORTED"
        assert data["listing_id"] == con_hang_agent_listing

    async def test_sold_out_with_notes_is_saved(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/sold-out",
            json={"notes": "Đã bán hết"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        assert response.json()["notes"] == "Đã bán hết"

    async def test_sold_out_on_da_coc_listing_returns_409(
        self, client: AsyncClient, agent_token: str, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/sold-out",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Listing must be in CON_HANG to report sold out"

    async def test_sold_out_on_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/deal-events/sold-out",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_report_sold_out(
        self, client: AsyncClient, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/sold-out",
            json={},
        )
        assert response.status_code == 401
