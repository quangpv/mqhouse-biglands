import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import AGENT_UUID

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
        assert data["requires_approval"] is False

    async def test_updating_price_on_CON_HANG_triggers_re_approval(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_con_hang}",
            json={"price": "9999999999"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING_APPROVAL"
        assert data["requires_approval"] is True

    async def test_updating_area_width_on_CON_HANG_triggers_re_approval(
        self, client: AsyncClient, admin_token: str, admin_con_hang: str,
    ) -> None:
        response = await client.put(
            f"/listings/{admin_con_hang}",
            json={"area_width": "10.0"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING_APPROVAL"
        assert data["requires_approval"] is True

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

    async def test_cannot_change_transaction_type_when_deposited(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str, db_session,
    ) -> None:
        from src.data.entities.listing import ListingStatus
        from sqlalchemy import select

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(agent_con_hang))
        )
        listing = result.scalar_one()
        listing.status = ListingStatus.DA_COC
        await db_session.flush()

        response = await client.put(
            f"/listings/{agent_con_hang}",
            json={"transaction_type": "CHO_THUE"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 400
        assert "deposited" in response.json()["detail"].lower()

    async def test_can_update_non_transaction_fields_when_deposited(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str, db_session,
    ) -> None:
        from src.data.entities.listing import ListingStatus
        from sqlalchemy import select

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(agent_con_hang))
        )
        listing = result.scalar_one()
        listing.status = ListingStatus.DA_COC
        await db_session.flush()

        response = await client.put(
            f"/listings/{agent_con_hang}",
            json={"description": "Updated after deposit"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated after deposit"

    async def test_unauthenticated_user_cannot_update_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.put(
            "/listings/00000000-0000-0000-0000-000000000099",
            json={"description": "No auth"},
        )
        assert response.status_code == 401
