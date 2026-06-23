from src.modules.geography.data import get_districts
from src.modules.geography.schemas import DistrictListResponse, DistrictResponse, WardResponse


async def get_districts_list(city_id: str) -> DistrictListResponse:
    districts = get_districts(city_id)
    return DistrictListResponse(
        data=[
            DistrictResponse(
                id=d["id"],
                name=d["name"],
                wards=[WardResponse(id=w["id"], name=w["name"]) for w in d["wards"]],
            )
            for d in districts
        ]
    )
