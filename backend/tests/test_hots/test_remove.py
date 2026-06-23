from datetime import datetime, timedelta, timezone

class TestRemoveFromHot:
    async def test_remove_hot_property_success(self, client, admin_token, test_property):
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

        resp = await client.delete(
            f"/properties/{prop_id}/hots",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 204

        hots_resp = await client.get("/properties/hots")
        assert hots_resp.json() == []

    async def test_remove_requires_admin_role(self, client, agent_token, test_property):
        resp = await client.delete(
            f"/properties/{test_property}/hots",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 403

    async def test_remove_not_hot(self, client, admin_token, test_property):
        resp = await client.delete(
            f"/properties/{test_property}/hots",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 404
