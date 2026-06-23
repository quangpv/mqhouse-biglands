import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_delete_transaction_type(client: AsyncClient, admin_token: str) -> None:
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "TO_DELETE", "display_name": "To Delete"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.delete(
        f"/transaction-types/{type_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_non_admin_cannot_delete_transaction_type(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "NO_DELETE", "display_name": "No Delete"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.delete(
        f"/transaction-types/{type_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.delete(
        f"/transaction-types/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_without_auth_fails(client: AsyncClient) -> None:
    response = await client.delete(f"/transaction-types/{uuid.uuid4()}")
    assert response.status_code == 401
