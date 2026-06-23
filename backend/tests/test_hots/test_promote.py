from datetime import datetime, timedelta, timezone

class TestPromoteToHot:
    async def test_promote_property_to_hot_success(self, client, admin_token, test_property):
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
        data = resp.json()
        assert data["property"]["id"] == str(prop_id)
        assert "start_time" in data
        assert "end_time" in data
        assert "id" in data

    async def test_promote_requires_admin_role(self, client, agent_token, test_property):
        now = datetime.now(timezone.utc)
        resp = await client.post(
            f"/properties/{test_property}/hots",
            json={
                "start_time": (now - timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
            },
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 403

    async def test_promote_unauthenticated(self, client, test_property):
        now = datetime.now(timezone.utc)
        resp = await client.post(
            f"/properties/{test_property}/hots",
            json={
                "start_time": (now - timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
            },
        )
        assert resp.status_code == 401

    async def test_promote_nonexistent_property(self, client, admin_token):
        now = datetime.now(timezone.utc)
        resp = await client.post(
            "/properties/00000000-0000-0000-0000-000000009999/hots",
            json={
                "start_time": (now - timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 404
