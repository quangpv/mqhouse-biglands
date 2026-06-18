import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestReportClosure:
    async def test_agent_reports_closure_on_da_coc_listing(
        self, client: AsyncClient, agent_token: str, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/closure",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "CLOSURE_REPORTED"
        assert data["listing_id"] == da_coc_agent_listing

    async def test_closure_on_con_hang_listing_returns_409(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/closure",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Listing must be in DA_COC to report a closure"

    async def test_closure_on_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/deal-events/closure",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_report_closure(
        self, client: AsyncClient, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/closure",
            json={},
        )
        assert response.status_code == 401

    async def test_closure_with_notes_is_saved(
        self, client: AsyncClient, agent_token: str, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/closure",
            json={"notes": "Đã hoàn tất thủ tục sang tên"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        assert response.json()["notes"] == "Đã hoàn tất thủ tục sang tên"
