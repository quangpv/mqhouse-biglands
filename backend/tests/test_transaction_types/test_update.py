import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_update_transaction_type(client: AsyncClient, admin_token: str) -> None:
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "OLD_CODE", "display_name": "Old Name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/transaction-types/{type_id}",
        json={"code": "NEW_CODE", "display_name": "New Name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "NEW_CODE"
    assert data["display_name"] == "New Name"


@pytest.mark.asyncio
async def test_non_admin_cannot_update_transaction_type(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "UPDATE_TEST", "display_name": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/transaction-types/{type_id}",
        json={"code": "HACKED", "display_name": "Hacked"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_nonexistent_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/transaction-types/{uuid.uuid4()}",
        json={"code": "NOPE", "display_name": "Nope"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_duplicate_code_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/transaction-types/",
        json={"code": "EXISTING", "display_name": "Existing"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    create_resp = await client.post(
        "/transaction-types/",
        json={"code": "TO_UPDATE", "display_name": "To Update"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/transaction-types/{type_id}",
        json={"code": "EXISTING", "display_name": "Conflict"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
