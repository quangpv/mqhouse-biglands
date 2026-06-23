


class TestListMyPins:
    async def test_list_my_pins_success(self, client, agent_token, test_property):
        await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        resp = await client.get(
            "/me/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == str(test_property)
        assert data["metadata"]["total_pages"] == 1

    async def test_list_my_pins_empty(self, client, agent_token):
        resp = await client.get(
            "/me/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["data"] == []

    async def test_list_my_pins_unauthenticated(self, client):
        resp = await client.get("/me/pins")
        assert resp.status_code == 401

    async def test_list_my_pins_shows_only_own_pins(self, client, agent_token, admin_token, test_property):
        await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        resp = await client.get(
            "/me/pins",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["data"] == []
