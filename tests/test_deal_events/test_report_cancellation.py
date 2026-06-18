import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestReportCancellation:
    async def test_agent_reports_cancellation_on_da_coc_listing_with_reason(
        self, client: AsyncClient, agent_token: str, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/cancellation",
            json={"notes": "Khách thay đổi ý định"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "CANCELLATION_REPORTED"
        assert data["notes"] == "Khách thay đổi ý định"
        assert data["listing_id"] == da_coc_agent_listing

    async def test_cancellation_without_reason_returns_422(
        self, client: AsyncClient, agent_token: str, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/cancellation",
            json={},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 422

    async def test_cancellation_on_con_hang_listing_returns_409(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/cancellation",
            json={"notes": "Lý do hủy"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Listing must be in DA_COC to report a cancellation"

    async def test_cancellation_on_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/deal-events/cancellation",
            json={"notes": "Lý do hủy"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_report_cancellation(
        self, client: AsyncClient, da_coc_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{da_coc_agent_listing}/deal-events/cancellation",
            json={"notes": "Lý do hủy"},
        )
        assert response.status_code == 401
