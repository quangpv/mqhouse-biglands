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
          {getTransactionTypeLabel(listing.transactionType)}
        </Badge>
        <Badge variant="outline" className="text-xs">
          {getPropertyTypeLabel(listing.propertyType)}
        </Badge>
      </div>
      <p className="text-2xl font-bold text-primary">
        {formatPrice(listing.price)}
      </p>
      {listing.pricePerM2 && (
        <p className="text-sm text-muted-foreground">
          {formatPrice(listing.pricePerM2)} /m²
        </p>
      )}
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <span className="text-muted-foreground">Diện tích: </span>
          <span className="font-medium">{formatArea(listing.totalArea)}</span>
          <span className="text-xs text-muted-foreground">
            {" "}({listing.areaWidth} × {listing.areaLength})
          </span>
        </div>
        <div>
          <span className="text-muted-foreground">Phòng ngủ: </span>
          <span className="font-medium">{listing.numRooms}</span>
        </div>
        <div>
          <span className="text-muted-foreground">Phòng tắm: </span>
          <span className="font-medium">{listing.numBathrooms}</span>
        </div>
        <div>
          <span className="text-muted-foreground">Số tầng: </span>
          <span className="font-medium">{listing.numFloors}</span>
        </div>
        <div className="col-span-2">
          <span className="text-muted-foreground">Địa chỉ: </span>
          <span className="font-medium">
            {listing.streetName}, {listing.ward}, {listing.district}, {listing.city}
          </span>
        </div>
      </div>
    </div>
  )
}
