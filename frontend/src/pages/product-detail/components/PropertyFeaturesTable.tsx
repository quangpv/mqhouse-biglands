import { formatPrice, formatArea } from "@/shared/utils"
import type { ListingDetailResponseDTO } from "@/data/types/listing.dto"

interface PropertyFeaturesTableProps {
  listing: ListingDetailResponseDTO
}

export function PropertyFeaturesTable({ listing }: PropertyFeaturesTableProps) {
  const rows: [string, string | number | null][] = [
    ["Mức giá", formatPrice(listing.price)],
    ["Diện tích", formatArea(listing.total_area)],
    ["Số phòng ngủ", listing.num_rooms],
    ["Số phòng tắm, vệ sinh", listing.num_bathrooms],
    ["Số tầng", listing.num_floors],
    ["Hướng nhà", listing.direction],
    ["Mặt tiền/Hẻm", listing.frontage_type],
    ["Đường vào", listing.road_width],
    ["Pháp lý", listing.legal_status],
    ["Nội thất", listing.furnishing ?? "—"],
  ]

  return (
    <div className="rounded-lg border">
      <table className="w-full text-sm">
        <tbody>
          {rows.map(([label, value], idx) => (
            <tr key={label} className={idx % 2 === 0 ? "bg-muted/30" : ""}>
              <td className="w-1/3 px-4 py-2 text-muted-foreground">{label}</td>
              <td className="px-4 py-2 font-medium">{value ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
