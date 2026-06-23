import pytest

pytestmark = pytest.mark.usefixtures("seed_lookups")


class TestCreateReview:
    async def test_create_review_success(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Great property!"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["content"] == "Great property!"
        assert data["property_id"] == str(prop_id)
        assert "id" in data
        assert data["images"] == []

    async def test_create_review_unauthenticated(self, client, reviewed_property):
        resp = await client.post(
            f"/properties/{reviewed_property}/reviews/",
            json={"content": "Should fail"},
        )
        assert resp.status_code == 401

    async def test_create_duplicate_review_fails(self, client, agent_token, reviewed_property):
        prop_id = reviewed_property
        resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "First review"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 201

        resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Second review"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 409

    async def test_create_review_on_nonexistent_property(self, client, agent_token):
        resp = await client.post(
            "/properties/00000000-0000-0000-0000-000000009999/reviews/",
            json={"content": "No property"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404

    async def test_create_review_different_users_can_review(self, client, agent_token, admin_token, reviewed_property):
        prop_id = reviewed_property
        resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Agent review"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 201

        resp = await client.post(
            f"/properties/{prop_id}/reviews/",
            json={"content": "Admin review"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 201
