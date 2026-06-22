from pydantic import BaseModel


class WardResponse(BaseModel):
    id: str
    name: str


class DistrictResponse(BaseModel):
    id: str
    name: str
    wards: list[WardResponse]


class CityResponse(BaseModel):
    id: str
    name: str
    districts: list[DistrictResponse]


class DistrictListResponse(BaseModel):
    data: list[DistrictResponse]


class WardListResponse(BaseModel):
    data: list[WardResponse]
