import { useQuery } from "@tanstack/react-query"
import { geographyRepository } from "@/data/repositories/geography.repository"
import { geographyQueries } from "@/data/queries/geography.queries"

interface LocationCascadeProps {
  city: string
  district: string
  ward: string
  onCityChange: (value: string) => void
  onDistrictChange: (value: string) => void
  onWardChange: (value: string) => void
  disabled?: boolean
}

export function LocationCascade({
  city,
  district,
  ward,
  onCityChange,
  onDistrictChange,
  onWardChange,
  disabled = false,
}: LocationCascadeProps) {
  const citiesQuery = useQuery({
    queryKey: geographyQueries.cities(),
    queryFn: geographyRepository.getCities,
  })

  const districtsQuery = useQuery({
    queryKey: geographyQueries.districts(city),
    queryFn: () => geographyRepository.getDistricts(city),
    enabled: !!city,
  })

  const wardsQuery = useQuery({
    queryKey: geographyQueries.wards(city, district),
    queryFn: () => geographyRepository.getWards(city, district),
    enabled: !!city && !!district,
  })

  function handleCityChange(e: React.ChangeEvent<HTMLSelectElement>) {
    onCityChange(e.target.value)
    onDistrictChange("")
    onWardChange("")
  }

  function handleDistrictChange(e: React.ChangeEvent<HTMLSelectElement>) {
    onDistrictChange(e.target.value)
    onWardChange("")
  }

  const cities = citiesQuery.data ?? []
  const districts = districtsQuery.data?.data ?? []
  const wards = wardsQuery.data?.data ?? []

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="space-y-2">
        <label className="text-sm font-medium">Thành phố / Tỉnh</label>
        <select
          className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
          value={city}
          onChange={handleCityChange}
          disabled={disabled || citiesQuery.isLoading}
        >
          <option value="">Chọn thành phố</option>
          {cities.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Quận / Huyện</label>
        <select
          className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
          value={district}
          onChange={handleDistrictChange}
          disabled={disabled || !city || districtsQuery.isLoading}
        >
          <option value="">Chọn quận</option>
          {districts.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Phường / Xã</label>
        <select
          className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
          value={ward}
          onChange={(e) => onWardChange(e.target.value)}
          disabled={disabled || !district || wardsQuery.isLoading}
        >
          <option value="">Chọn phường</option>
          {wards.map((w) => (
            <option key={w.id} value={w.id}>
              {w.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
