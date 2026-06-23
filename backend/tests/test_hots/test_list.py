from datetime import datetime, timedelta, timezone

class TestListHotProperties:
    async def test_list_active_hot_properties(self, client, admin_token, test_property):
        prop_id = test_property
        now = datetime.now(timezone.utc)
        resp = await client.post(
            f"/properties/{prop_id}/hots",
            json={
                "start_time": (now - timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 201

        resp = await client.get("/properties/hots")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["property"]["id"] == str(prop_id)

    async def test_list_returns_empty_when_no_hot_properties(self, client):
        resp = await client.get("/properties/hots")
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_excludes_expired_hot_properties(self, client, admin_token, test_property):
        prop_id = test_property
        now = datetime.now(timezone.utc)
        resp = await client.post(
            f"/properties/{prop_id}/hots",
            json={
                "start_time": (now - timedelta(hours=2)).isoformat(),
                "end_time": (now - timedelta(hours=1)).isoformat(),
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 201

        resp = await client.get("/properties/hots")
        assert resp.json() == []

    async def test_list_is_public(self, client, admin_token, test_property):
        prop_id = test_property
        now = datetime.now(timezone.utc)
        await client.post(
            f"/properties/{prop_id}/hots",
            json={
                "start_time": (now - timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        resp = await client.get("/properties/hots")
        assert resp.status_code == 200
