import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestListMyProperties:
    async def test_list_my_properties_pagination(self, client, admin_token, property_payload):
        for i in range(3):
            p = {**property_payload, "title": f"Property {i}"}
            await client.post("/properties", json=p, headers={"Authorization": f"Bearer {admin_token}"})

        resp = await client.get(
            "/me/properties?page=1&size=2",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["data"]) <= 2
        assert data["metadata"]["page"] == 1
        assert data["metadata"]["size"] == 2
        assert data["metadata"]["total_pages"] >= 1

    async def test_list_my_properties_shows_only_own(self, client, admin_token, agent_token, property_payload):
        await client.post(
            "/properties",
            json=property_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        resp = await client.get(
            "/me/properties",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["data"] == []

    async def test_list_my_properties_filter_by_status(self, client, admin_token, property_payload):
        payload = {**property_payload, "type": "post_pending"}
        await client.post("/properties", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

        resp = await client.get(
            "/me/properties?status=post_pending",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        for p in resp.json()["data"]:
            assert p["status"] == "post_pending"

    async def test_list_my_properties_filter_by_district(self, client, admin_token, property_payload):
        payload = {**property_payload, "district": "District 2"}
        await client.post("/properties", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

        resp = await client.get(
            "/me/properties?district=District+2",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        for p in resp.json()["data"]:
            assert p["district"] == "District 2"

    async def test_list_my_properties_filter_by_price_range(self, client, admin_token, property_payload):
        cheap = {**property_payload, "price": 1000000}
        expensive = {**property_payload, "price": 100000000}
        await client.post("/properties", json=cheap, headers={"Authorization": f"Bearer {admin_token}"})
        await client.post("/properties", json=expensive, headers={"Authorization": f"Bearer {admin_token}"})

        resp = await client.get(
            "/me/properties?price_from=50000000",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        for p in resp.json()["data"]:
            assert float(p["price"]) >= 50000000

    async def test_list_my_properties_search(self, client, admin_token, property_payload):
        unique = {**property_payload, "title": "Skyline Penthouse 999"}
        await client.post("/properties", json=unique, headers={"Authorization": f"Bearer {admin_token}"})

        resp = await client.get(
            "/me/properties?search=Skyline",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        assert any("Skyline" in (p.get("title") or "") for p in resp.json()["data"])

    async def test_list_my_properties_unauthenticated(self, client):
        resp = await client.get("/me/properties")
        assert resp.status_code == 401
