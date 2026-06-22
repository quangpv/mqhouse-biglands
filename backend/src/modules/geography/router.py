from fastapi import APIRouter, Depends

from src.modules.geography.facades.get_cities import get_cities_list
from src.modules.geography.facades.get_districts import get_districts_list
from src.modules.geography.facades.get_wards import get_wards_list
from src.modules.geography.schemas import CityResponse, DistrictListResponse, WardListResponse

router = APIRouter(prefix="/geography", tags=["geography"])


@router.get("/cities", response_model=list[CityResponse])
async def list_cities(result: list[CityResponse] = Depends(get_cities_list)):
    return result


@router.get("/cities/{city_id}/districts", response_model=DistrictListResponse)
async def list_districts(result: DistrictListResponse = Depends(get_districts_list)):
    return result


@router.get("/cities/{city_id}/districts/{district_id}/wards", response_model=WardListResponse)
async def list_wards(result: WardListResponse = Depends(get_wards_list)):
    return result
