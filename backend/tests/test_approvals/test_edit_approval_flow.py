import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity

pytestmark = pytest.mark.asyncio

MINIMAL = {
    "property_type": "CHDV",
    "description": "End-to-end business rules test",
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


class TestBusinessRules:
    async def test_create_submit_approve_update_deposit_guard_flow(
        self,
        client: AsyncClient,
        agent_token: str,
        admin_token: str,
        db_session: AsyncSession,
    ) -> None:
        # ── 1. Agent creates + submits → PENDING_APPROVAL (v1) ──────────
        payload = {**MINIMAL, "action": "submit", "description": "Full cycle test"}
        response = await client.post(
            "/listings",
            json=payload,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        listing_id = response.json()["id"]
        assert response.json()["status"] == "PENDING_APPROVAL"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.approval_version == 1

        # ── 2. Admin approves → CON_HANG ────────────────────────────────
        response = await client.post(
            f"/approvals/{listing_id}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "CON_HANG"

        # ── 3. Agent edits non-critical field → stays CON_HANG, version unchanged ──
        response = await client.put(
            f"/listings/{listing_id}",
            json={"description": "Updated after approval"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "CON_HANG"
        assert data["description"] == "Updated after approval"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.approval_version == 1

        # ── 4. Agent reports deposit → stays CON_HANG ───────────────────#
        response = await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={
                "customer_name": "Nguyễn Văn A",
                "customer_phone": "0909123456",
                "deposit_amount": "100000000",
            },
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        assert response.json()["event_type"] == "DEPOSIT_REPORTED"

        # ── 5. Agent tries critical-field edit → blocked by deposit orphan guard ──
        response = await client.put(
            f"/listings/{listing_id}",
            json={"price": "9999999999"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 400
        assert "deposit" in response.json()["detail"].lower()

        # ── 6. Admin approves deposit → DA_COC ───────────────────────────
        response = await client.post(
            f"/approvals/{listing_id}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "DA_COC"

        # ── 7. Agent edits non-critical field on DA_COC → stays DA_COC ───
        response = await client.put(
            f"/listings/{listing_id}",
            json={"description": "Edit after deposit approved"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "DA_COC"
        assert response.json()["description"] == "Edit after deposit approved"
