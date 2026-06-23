import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_get_transaction_type(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "BAN", "display_name": "Bán"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.get(
        f"/transaction-types/{type_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "BAN"
    assert data["display_name"] == "Bán"


@pytest.mark.asyncio
async def test_get_nonexistent_transaction_type_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        f"/transaction-types/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_transaction_type_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get(f"/transaction-types/{uuid.uuid4()}")
    assert response.status_code == 401
