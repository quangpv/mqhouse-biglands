import httpClient from "../infra/http-client"
import type { CityDTO, DistrictListResponseDTO, WardListResponseDTO } from "../types/geography.dto"

export const geographyRepository = {
  getCities: () =>
    httpClient.get<CityDTO[]>("/geography/cities").then((r) => r.data),

  getDistricts: (cityId: string) =>
    httpClient.get<DistrictListResponseDTO>(`/geography/cities/${cityId}/districts`).then((r) => r.data),

  getWards: (cityId: string, districtId: string) =>
    httpClient.get<WardListResponseDTO>(`/geography/cities/${cityId}/districts/${districtId}/wards`).then((r) => r.data),
}
