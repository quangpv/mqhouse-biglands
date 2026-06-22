export const geographyQueries = {
  all: ["geography"] as const,
  cities: () => [...geographyQueries.all, "cities"] as const,
  districts: (cityId: string) => [...geographyQueries.all, "districts", cityId] as const,
  wards: (cityId: string, districtId: string) =>
    [...geographyQueries.all, "wards", cityId, districtId] as const,
}
