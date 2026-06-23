import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestDeleteReview:
    async def test_delete_own_review(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Will delete"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.delete(
            f"/properties/{prop_id}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 204

        resp = await client.get(
            f"/properties/{prop_id}/reviews/",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert len(resp.json()["data"]) == 0

    async def test_delete_as_admin(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Admin delete"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.delete(
            f"/properties/{prop_id}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 204

    async def test_delete_others_review_fails(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Owned by admin"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.delete(
            f"/properties/{prop_id}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 403

    async def test_delete_nonexistent_review(self, client, agent_token, reviewed_property):
        resp = await client.delete(
            f"/properties/{reviewed_property}/reviews/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404

    async def test_delete_unauthenticated(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        create_resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "No auth"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        review_id = create_resp.json()["id"]

        resp = await client.delete(f"/properties/{prop_id}/reviews/{review_id}")
        assert resp.status_code == 401
