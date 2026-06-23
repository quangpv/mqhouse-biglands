


class TestRemovePin:
    async def test_remove_pin_success(self, client, agent_token, test_property):
        await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        resp = await client.delete(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 204

    async def test_remove_pin_unauthenticated(self, client, test_property):
        resp = await client.delete(f"/properties/{test_property}/pins")
        assert resp.status_code == 401

    async def test_remove_not_pinned(self, client, agent_token, test_property):
        resp = await client.delete(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404
