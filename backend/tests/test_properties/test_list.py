import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_list_properties_pagination(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    for i in range(3):
        p = {**property_payload, "title": f"Property {i}"}
        await client.post("/properties", json=p, headers={"Authorization": f"Bearer {admin_token}"})

    response = await client.get(
        "/properties?page=1&size=2",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) <= 2
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["size"] == 2
    assert data["metadata"]["total_pages"] >= 1


@pytest.mark.asyncio
async def test_list_properties_filter_by_status(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    payload = {**property_payload, "type": "post_pending"}
    await client.post("/properties", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

    response = await client.get(
        "/properties?status=post_pending",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    for p in response.json()["data"]:
        assert p["status"] == "post_pending"


@pytest.mark.asyncio
async def test_list_properties_filter_by_district(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    payload = {**property_payload, "district": "District 2"}
    await client.post("/properties", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

    response = await client.get(
        "/properties?district=District+2",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    for p in response.json()["data"]:
        assert p["district"] == "District 2"


@pytest.mark.asyncio
async def test_list_properties_filter_by_price_range(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    cheap = {**property_payload, "price": 1000000}
    expensive = {**property_payload, "price": 100000000}
    await client.post("/properties", json=cheap, headers={"Authorization": f"Bearer {admin_token}"})
    await client.post("/properties", json=expensive, headers={"Authorization": f"Bearer {admin_token}"})

    response = await client.get(
        "/properties?price_from=5000000&price_to=50000000",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    for p in response.json()["data"]:
        assert 5000000 <= p["price"] <= 50000000


@pytest.mark.asyncio
async def test_list_properties_sort_by_price_asc(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    cheap = {**property_payload, "title": "cheap", "price": 1000000}
    expensive = {**property_payload, "title": "expensive", "price": 9999999999}
    await client.post("/properties", json=cheap, headers={"Authorization": f"Bearer {admin_token}"})
    await client.post("/properties", json=expensive, headers={"Authorization": f"Bearer {admin_token}"})

    response = await client.get(
        "/properties?sort_by=price&sort_order=asc&size=10",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    prices = [p["price"] for p in data if p["title"] in ("cheap", "expensive")]
    assert prices == sorted(prices)


@pytest.mark.asyncio
async def test_list_properties_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/properties")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_properties_empty_result(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/properties?search=NONEXISTENT",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["metadata"]["total_pages"] == 0
