import uuid

import pytest
from httpx import AsyncClient

from tests.test_approvals.conftest import _make_listing
from src.data.entities.listing import ListingStatus
from tests.conftest import AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestBulkApprove:
    async def test_bulk_approve_all_listings_succeed(
        self, client: AsyncClient, admin_token: str, db_session,
    ) -> None:
        id1 = str(uuid.uuid4())
        id2 = str(uuid.uuid4())
        listing1 = _make_listing(AGENT_UUID, ListingStatus.PENDING_APPROVAL)
        listing1.id = uuid.UUID(id1)
        listing2 = _make_listing(AGENT_UUID, ListingStatus.PENDING_APPROVAL)
        listing2.id = uuid.UUID(id2)
        db_session.add_all([listing1, listing2])
        await db_session.flush()

        response = await client.post(
            "/approvals/bulk-approve",
            json={"listing_ids": [id1, id2]},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["succeeded"] == 2
        assert data["failed"] == 0
        assert data["total"] == 2

    async def test_bulk_approve_partial_failure(
        self, client: AsyncClient, admin_token: str, db_session, pending_approval_listing: str,
    ) -> None:
        draft_id = str(uuid.uuid4())
        draft = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
        draft.id = uuid.UUID(draft_id)
        db_session.add(draft)
        await db_session.flush()

        response = await client.post(
            "/approvals/bulk-approve",
            json={"listing_ids": [pending_approval_listing, draft_id]},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["succeeded"] == 1
        assert data["failed"] == 1
        assert data["total"] == 2

    async def test_bulk_approve_empty_list_returns_422(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/approvals/bulk-approve",
            json={"listing_ids": []},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 422

    async def test_agent_cannot_bulk_approve(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            "/approvals/bulk-approve",
            json={"listing_ids": [str(uuid.uuid4())]},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_user_cannot_bulk_approve(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/approvals/bulk-approve",
            json={"listing_ids": [str(uuid.uuid4())]},
        )
        assert response.status_code == 401
