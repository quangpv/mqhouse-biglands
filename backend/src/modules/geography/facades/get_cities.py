from src.modules.geography.data import get_cities
from src.modules.geography.schemas import CityResponse


async def get_cities_list() -> list[CityResponse]:
    cities = get_cities()
    return [CityResponse(**city) for city in cities]
