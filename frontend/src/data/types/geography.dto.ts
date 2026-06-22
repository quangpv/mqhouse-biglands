export interface WardDTO {
  id: string
  name: string
}

export interface DistrictDTO {
  id: string
  name: string
  wards: WardDTO[]
}

export interface CityDTO {
  id: string
  name: string
  districts: DistrictDTO[]
}

export interface DistrictListResponseDTO {
  data: DistrictDTO[]
}

export interface WardListResponseDTO {
  data: WardDTO[]
}
