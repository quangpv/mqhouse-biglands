import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestReportDeposit:
    async def test_agent_reports_deposit_on_con_hang_listing(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "DEPOSIT_REPORTED"
        assert data["customer_name"] == "Nguyễn Văn A"
        assert data["deposit_amount"] == "100000000"
        assert data["listing_id"] == con_hang_agent_listing

    async def test_deposit_with_phone_and_notes_saves_all_info(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={
                "customer_name": "Trần Thị B",
                "customer_phone": "0987654321",
                "deposit_amount": "200000000",
                "notes": "Khách đã xem nhà và đặt cọc",
            },
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["customer_name"] == "Trần Thị B"
        assert data["customer_phone"] == "0987654321"
        assert data["deposit_amount"] == "200000000"
        assert data["notes"] == "Khách đã xem nhà và đặt cọc"

    async def test_deposit_on_draft_listing_returns_409(
        self, client: AsyncClient, agent_token: str, draft_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{draft_agent_listing}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Listing must be in CON_HANG to report a deposit"

    async def test_duplicate_active_deposit_returns_409(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={"customer_name": "Lê Văn C", "deposit_amount": "200000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "An active deposit already exists for this listing"

    async def test_deposit_on_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_report_deposit(
        self, client: AsyncClient, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
        )
        assert response.status_code == 401

    async def test_deposit_with_short_name_returns_422(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{con_hang_agent_listing}/deal-events/deposit",
            json={"customer_name": "A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 422
