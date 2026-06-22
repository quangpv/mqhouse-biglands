import { Link } from "react-router-dom"
import { Card } from "@/shared/components/ui/card"
import { Badge } from "@/shared/components/ui/badge"
import { Skeleton } from "@/shared/components/ui/skeleton"
import { formatPrice, getStatusLabel, getStatusColor, getTransactionTypeLabel, getPropertyTypeLabel, formatArea } from "@/shared/utils"
import type { ListingDTO } from "@/data/types/listing.dto"

interface ListingCardProps {
  listing: ListingDTO
}

export function ListingCard({ listing }: ListingCardProps) {
  return (
    <Link to={`/tin/${listing.id}`} className="block">
      <Card className="flex-row gap-4 overflow-hidden p-4">
        <div className="relative h-32 w-40 shrink-0 overflow-hidden rounded-lg bg-muted">
          {listing.primaryImageUrl ? (
            <img
              src={listing.primaryImageUrl}
              alt=""
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-muted-foreground text-sm">
              No Image
            </div>
          )}
          {listing.isHot && (
            <Badge className="absolute top-1 left-1 bg-red-500 text-white text-[10px] px-1.5 py-0">
              Hot
            </Badge>
          )}
        </div>
        <div className="flex min-w-0 flex-1 flex-col justify-between gap-1">
          <div className="space-y-1">
            <p className="text-sm font-semibold leading-tight truncate">
              {listing.title || listing.address}
            </p>
            <p className="text-base font-bold text-primary">
              {formatPrice(listing.price, { compact: true })}
            </p>
            <div className="flex flex-wrap gap-1">
              <Badge variant="outline" className="text-[10px]">
                {getTransactionTypeLabel(listing.transactionType)}
              </Badge>
              <Badge variant="outline" className="text-[10px]">
                {getPropertyTypeLabel(listing.propertyType)}
              </Badge>
              <Badge variant="outline" className="text-[10px]">
                {formatArea(listing.totalArea)}
              </Badge>
            </div>
          </div>
          <div className="flex items-center justify-between gap-2">
            <span className="text-xs text-muted-foreground truncate">
              {listing.district}, {listing.city}
            </span>
            <div className={`h-2 w-2 rounded-full ${getStatusColor(listing.status)}`} title={getStatusLabel(listing.status)} />
          </div>
        </div>
      </Card>
    </Link>
  )
}

export function ListingCardSkeleton() {
  return (
    <Card className="flex-row gap-4 overflow-hidden p-4">
      <Skeleton className="h-32 w-40 shrink-0 rounded-lg" />
      <div className="flex min-w-0 flex-1 flex-col justify-between gap-2">
        <div className="space-y-2">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-5 w-1/3" />
          <div className="flex gap-1">
            <Skeleton className="h-4 w-12" />
            <Skeleton className="h-4 w-12" />
            <Skeleton className="h-4 w-16" />
          </div>
        </div>
        <Skeleton className="h-3 w-1/2" />
      </div>
    </Card>
  )
}
