import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestListReviews:
    async def test_list_reviews_empty(self, client, agent_token, reviewed_property):
        resp = await client.get(
            f"/properties/{reviewed_property}/reviews/",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["data"] == []
        assert data["metadata"]["total_pages"] == 0

    async def test_list_reviews_after_creation(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Great!"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Awesome!"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        resp = await client.get(
            f"/properties/{prop_id}/reviews/",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["data"]) == 2
        assert data["metadata"]["total_pages"] == 1

    async def test_list_reviews_pagination(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "One"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Two"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        resp = await client.get(
            f"/properties/{prop_id}/reviews/",
            params={"page": 1, "size": 1},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["data"]) == 1
        assert data["metadata"]["total_pages"] == 2

    async def test_list_reviews_unauthenticated(self, client, reviewed_property):
        resp = await client.get(f"/properties/{reviewed_property}/reviews/")
        assert resp.status_code == 401

    async def test_list_reviews_nonexistent_property(self, client, agent_token):
        resp = await client.get(
            "/properties/00000000-0000-0000-0000-000000009999/reviews/",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404
