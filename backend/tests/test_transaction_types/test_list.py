import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_list_transaction_types(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/transaction-types/",
        json={"code": "BAN", "display_name": "Bán"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/transaction-types/",
        json={"code": "CHO_THUE", "display_name": "Cho thuê"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/transaction-types/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    codes = [item["code"] for item in data]
    assert "BAN" in codes
    assert "CHO_THUE" in codes


@pytest.mark.asyncio
async def test_list_transaction_types_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/transaction-types/")
    assert response.status_code == 401
