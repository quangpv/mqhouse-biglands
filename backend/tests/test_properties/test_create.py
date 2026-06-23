
import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID




@pytest.mark.asyncio
async def test_create_property_draft(client: AsyncClient, agent_token: str, property_payload: dict) -> None:
    response = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] is not None
    assert data["description"] == "A nice property"
    assert data["status"] == "draft"
    assert data["address"] == "123 Main Street, Ward 1"
    assert data["num_rooms"] == 3
    assert data["primary_image_url"] is None
    assert data["images"] == []
    assert data["is_pinned"] is False
    assert data["requires_approval"] is False
    assert data["price_per_m2"] is not None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_property_post_pending(client: AsyncClient, agent_token: str, property_payload: dict) -> None:
    payload = {**property_payload, "type": "post_pending"}
    response = await client.post(
        "/properties",
        json=payload,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "post_pending"
    assert data["requires_approval"] is True


@pytest.mark.asyncio
async def test_create_property_with_images(client: AsyncClient, admin_token: str, property_payload: dict,
                                           db_session) -> None:
    from uuid import uuid4
    from src.data.entities.file import EntityType, FileEntity
    file = FileEntity(id=uuid4(), origin_name="test.jpg", path="/uploads/test.jpg", mimetype="image/jpeg",
                      size=1024, entity_type=EntityType.PROPERTY, created_by_id=ADMIN_UUID)
    db_session.add(file)
    await db_session.commit()
    await db_session.refresh(file)
    assert file.id is not None, "File ID should be set after commit"

    payload = {**property_payload, "image_ids": [str(file.id)]}
    response = await client.post(
        "/properties",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["images"]) == 1, f"Expected 1 image, got {len(data['images'])}. Response: {data}"
    assert data["images"][0]["origin_name"] == "test.jpg"
    assert data["primary_image_url"] == "/uploads/test.jpg"


@pytest.mark.asyncio
async def test_create_property_unauthorized(client: AsyncClient, property_payload: dict) -> None:
    response = await client.post("/properties", json=property_payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_property_missing_required_fields(client: AsyncClient, agent_token: str) -> None:
    response = await client.post(
        "/properties",
        json={"type": "draft"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 422
