import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestReviewDetail:
    async def test_get_review_detail(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Detail test"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.get(
            f"/properties/{prop_id}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] == "Detail test"
        assert data["property_id"] == str(prop_id)

    async def test_get_nonexistent_review(self, client, agent_token, reviewed_property):
        resp = await client.get(
            f"/properties/{reviewed_property}/reviews/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404

    async def test_get_review_unauthenticated(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Auth test"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.get(f"/properties/{prop_id}/reviews/{review_id}")
        assert resp.status_code == 401

    async def test_get_review_wrong_property(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Wrong prop"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.get(
            f"/properties/00000000-0000-0000-0000-000000009999/reviews/{review_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 404
