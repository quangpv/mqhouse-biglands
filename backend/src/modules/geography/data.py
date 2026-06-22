import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "ho-chi-minh.json"


def _load_data() -> dict:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_cities() -> list[dict]:
    return _load_data()["cities"]


def get_city(city_id: str) -> dict | None:
    for city in get_cities():
        if city["id"] == city_id:
            return city
    return None


def get_districts(city_id: str) -> list[dict]:
    city = get_city(city_id)
    return city["districts"] if city else []


def get_district(city_id: str, district_id: str) -> dict | None:
    for district in get_districts(city_id):
        if district["id"] == district_id:
            return district
    return None


def get_wards(city_id: str, district_id: str) -> list[dict]:
    district = get_district(city_id, district_id)
    return district["wards"] if district else []
