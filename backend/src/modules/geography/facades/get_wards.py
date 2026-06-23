from fastapi import Path

from src.modules.geography.data import get_wards
from src.modules.geography.schemas import WardListResponse, WardResponse


async def get_wards_list(
    city_id: str = Path(...),
    district_id: str = Path(...),
) -> WardListResponse:
    wards = get_wards(city_id, district_id)
    return WardListResponse(data=[WardResponse(id=w["id"], name=w["name"]) for w in wards])
