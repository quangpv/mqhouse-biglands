import { Badge } from "@/shared/components/ui/badge"
import { formatPrice, formatArea, getTransactionTypeLabel, getPropertyTypeLabel } from "@/shared/utils"
import type { ListingDetailResponseDTO } from "@/data/types/listing.dto"

interface KeyInfoSectionProps {
  listing: ListingDetailResponseDTO
}

export function KeyInfoSection({ listing }: KeyInfoSectionProps) {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="outline" className="text-xs">
          {getTransactionTypeLabel(listing.transaction_type)}
        </Badge>
        <Badge variant="outline" className="text-xs">
          {getPropertyTypeLabel(listing.property_type)}
        </Badge>
      </div>
      <p className="text-2xl font-bold text-primary">
        {formatPrice(listing.price)}
      </p>
      {listing.price_per_m2 && (
        <p className="text-sm text-muted-foreground">
          {formatPrice(listing.price_per_m2)} /m²
        </p>
      )}
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <span className="text-muted-foreground">Diện tích: </span>
          <span className="font-medium">{formatArea(listing.total_area)}</span>
          <span className="text-xs text-muted-foreground">
            {" "}({listing.area_width} × {listing.area_length})
          </span>
        </div>
        <div>
          <span className="text-muted-foreground">Phòng ngủ: </span>
          <span className="font-medium">{listing.num_rooms}</span>
        </div>
        <div>
          <span className="text-muted-foreground">Phòng tắm: </span>
          <span className="font-medium">{listing.num_bathrooms}</span>
        </div>
        <div>
          <span className="text-muted-foreground">Số tầng: </span>
          <span className="font-medium">{listing.num_floors}</span>
        </div>
        <div className="col-span-2">
          <span className="text-muted-foreground">Địa chỉ: </span>
          <span className="font-medium">
            {listing.street_name}, {listing.ward}, {listing.district}, {listing.city}
          </span>
        </div>
      </div>
    </div>
  )
}
