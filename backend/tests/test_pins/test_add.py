import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestAddPin:
    async def test_add_pin_success(self, client, agent_token, test_property):
        resp = await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 201
        assert resp.json() == {"message": "Pinned"}

    async def test_add_pin_unauthenticated(self, client, test_property):
        resp = await client.post(f"/properties/{test_property}/pins")
        assert resp.status_code == 401

    async def test_add_duplicate_pin_fails(self, client, agent_token, test_property):
        resp = await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 201

        resp = await client.post(
            f"/properties/{test_property}/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 409

    async def test_add_pin_nonexistent_property(self, client, agent_token):
        resp = await client.post(
            "/properties/00000000-0000-0000-0000-000000009999/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404
