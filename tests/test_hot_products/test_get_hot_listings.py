import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import ADMIN_UUID

pytestmark = pytest.mark.asyncio


class TestGetHotListings:
    async def test_hot_listings_appear_in_public_list_ordered_by_position(
        self, client: AsyncClient, db_session,
    ) -> None:
        listing1 = _make_listing(ADMIN_UUID, "B")
        listing1.is_hot = True
        listing1.hot_order = 3
        listing2 = _make_listing(ADMIN_UUID, "A")
        listing2.is_hot = True
        listing2.hot_order = 1
        listing3 = _make_listing(ADMIN_UUID, "C")
        listing3.is_hot = True
        listing3.hot_order = 2
        db_session.add_all([listing1, listing2, listing3])
        await db_session.flush()

        response = await client.get("/hot-listings")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["hot_order"] == 1
        assert data[1]["hot_order"] == 2
        assert data[2]["hot_order"] == 3

    async def test_empty_hot_list_returns_empty_array(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/hot-listings")
        assert response.status_code == 200
        assert response.json() == []

    async def test_hot_list_endpoint_is_publicly_accessible(
        self, client: AsyncClient, hot_listing: str,
    ) -> None:
        response = await client.get("/hot-listings")
        assert response.status_code == 200

    async def test_non_hot_listings_are_excluded_from_hot_list(
        self, client: AsyncClient, db_session,
    ) -> None:
        hot = _make_listing(ADMIN_UUID, "hot")
        hot.is_hot = True
        hot.hot_order = 1
        normal = _make_listing(ADMIN_UUID, "normal")
        db_session.add_all([hot, normal])
        await db_session.flush()

        response = await client.get("/hot-listings")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["hot_order"] is not None


def _make_listing(owner_id, suffix):
    return ListingEntity(
        id=uuid.uuid4(),
        code=generate_product_code(),
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Hot test listing {suffix}",
        price=Decimal("5000000000"),
        commission_type=CommissionType.PERCENTAGE,
        commission_value=Decimal("1.5"),
        area_width=Decimal("5.0"),
        area_length=Decimal("20.0"),
        total_area=Decimal("100.0"),
        street_name="Lê Lợi",
        house_number="45",
        address=f"45 Lê Lợi, {suffix}",
        ward="Bến Nghé",
        district="Quận 1",
        city="Hồ Chí Minh",
        owner_phone="0900000001",
        created_by_id=owner_id,
        status=ListingStatus.CON_HANG,
    )
