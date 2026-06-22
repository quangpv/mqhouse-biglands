from src.modules.geography.data import get_districts
from src.modules.geography.schemas import DistrictListResponse


async def get_districts_list(city_id: str) -> DistrictListResponse:
    districts = get_districts(city_id)
    return DistrictListResponse(
        data=[{"id": d["id"], "name": d["name"], "wards": d["wards"]} for d in districts]
    )
