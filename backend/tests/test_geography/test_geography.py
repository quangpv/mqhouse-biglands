import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListCities:
    async def test_returns_hcm_as_only_city(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == "hcm"
        assert data[0]["name"] == "Hồ Chí Minh"

    async def test_city_contains_districts_with_wards(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities")
        data = response.json()
        hcm = data[0]
        assert "districts" in hcm
        assert len(hcm["districts"]) == 24
        assert all("wards" in d for d in hcm["districts"])

    async def test_endpoint_is_publicly_accessible(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities")
        assert response.status_code == 200


class TestListDistricts:
    async def test_returns_districts_for_hcm(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 24

    async def test_district_has_wards_field(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts")
        data = response.json()["data"]
        assert all("wards" in d for d in data)

    async def test_returns_empty_for_unknown_city(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/unknown/districts")
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []

    async def test_q1_has_10_wards(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts")
        data = response.json()["data"]
        q1 = next(d for d in data if d["id"] == "q1")
        assert len(q1["wards"]) == 10


class TestListWards:
    async def test_returns_wards_for_q1(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts/q1/wards")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 10

    async def test_ward_has_id_and_name(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts/q1/wards")
        ward = response.json()["data"][0]
        assert "id" in ward
        assert "name" in ward

    async def test_returns_empty_for_unknown_district(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/hcm/districts/unknown/wards")
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []

    async def test_returns_empty_for_unknown_city(self, client: AsyncClient) -> None:
        response = await client.get("/geography/cities/unknown/districts/unknown/wards")
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []
