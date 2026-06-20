import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

MINIMAL = {
    "property_type": "CHDV",
    "description": "Căn hộ dịch vụ cao cấp quận 1",
    "price": "5000000000",
    "commission_type": "PERCENTAGE",
    "commission_value": "1.5",
    "area_width": "5.5",
    "area_length": "20.0",
    "total_area": "110.0",
    "street_name": "Nguyễn Huệ",
    "house_number": "123",
    "address": "123 Nguyễn Huệ, Phường Bến Nghé, Quận 1",
    "ward": "Bến Nghé",
    "district": "Quận 1",
    "owner_phone": "0912345678",
}


class TestCreateListing:
    async def test_agent_can_create_a_listing_with_minimal_required_fields(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            "/listings",
            json=MINIMAL,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["property_type"] == "CHDV"
        assert data["description"] == MINIMAL["description"]
        assert data["status"] == "DRAFT"
        assert data["created_by_id"] is not None
        assert data["code"] is not None

    async def test_agent_can_create_and_submit_listing_in_one_action(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        payload = {**MINIMAL, "action": "submit", "description": "Submit in one go"}
        response = await client.post(
            "/listings",
            json=payload,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "PENDING_APPROVAL"

    async def test_admin_auto_approves_listing_as_con_hang(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {**MINIMAL, "description": "Admin creates"}
        response = await client.post(
            "/listings",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "CON_HANG"
        assert data["approved_by_id"] is not None

    async def test_approver_can_create_a_draft_listing(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {**MINIMAL, "description": "Approver creates"}
        response = await client.post(
            "/listings",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201

    async def test_create_listing_with_missing_required_field_returns_422(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        payload = {k: v for k, v in MINIMAL.items() if k != "property_type"}
        response = await client.post(
            "/listings",
            json=payload,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 422

    async def test_unauthenticated_user_cannot_create_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post("/listings", json=MINIMAL)
        assert response.status_code == 401
