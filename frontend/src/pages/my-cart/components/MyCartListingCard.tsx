import { useNavigate, Link } from "react-router-dom"
import { Card } from "@/shared/components/ui/card"
import { Badge } from "@/shared/components/ui/badge"
import { Button } from "@/shared/components/ui/button"
import { Skeleton } from "@/shared/components/ui/skeleton"
import {
  formatPrice,
  getStatusLabel,
  getStatusColor,
  getTransactionTypeLabel,
  getPropertyTypeLabel,
  formatArea,
} from "@/shared/utils"
import type { ListingDTO } from "@/data/types/listing.dto"
import { Edit, Trash2, ArrowLeftFromLine } from "lucide-react"

interface MyCartListingCardProps {
  listing: ListingDTO
  onDelete: (id: string) => void
  onWithdraw: (id: string) => void
  isDeleting?: boolean
  isWithdrawing?: boolean
}

export function MyCartListingCard({
  listing,
  onDelete,
  onWithdraw,
  isDeleting,
  isWithdrawing,
}: MyCartListingCardProps) {
  const navigate = useNavigate()

  const canEdit = listing.status === "DRAFT" || listing.status === "CON_HANG"
  const canDelete = listing.status === "DRAFT"
  const canWithdraw = listing.status === "CON_HANG"

  return (
    <Card className="flex-row gap-4 overflow-hidden p-4">
      <div
        className="relative h-32 w-40 shrink-0 overflow-hidden rounded-lg bg-muted cursor-pointer"
        onClick={() => navigate(`/tin/${listing.id}`)}
      >
        {listing.primary_image_url ? (
          <img src={listing.primaryImageUrl} alt="" className="h-full w-full object-cover" />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-muted-foreground text-sm">
            No Image
          </div>
        )}
        {listing.is_hot && (
          <Badge className="absolute top-1 left-1 bg-red-500 text-white text-[10px] px-1.5 py-0">
            Hot
          </Badge>
        )}
      </div>
      <div className="flex min-w-0 flex-1 flex-col justify-between gap-1">
        <Link to={`/tin/${listing.id}`} className="space-y-1">
          <p className="text-sm font-semibold leading-tight truncate">
            {listing.title || listing.address}
          </p>
          <p className="text-base font-bold text-primary">
            {formatPrice(listing.price, { compact: true })}
          </p>
          <div className="flex flex-wrap gap-1">
            <Badge variant="outline" className="text-[10px]">
              {getTransactionTypeLabel(listing.transaction_type)}
            </Badge>
            <Badge variant="outline" className="text-[10px]">
              {getPropertyTypeLabel(listing.property_type)}
            </Badge>
            <Badge variant="outline" className="text-[10px]">
              {formatArea(listing.total_area)}
            </Badge>
          </div>
        </Link>
        <div className="flex items-center justify-between gap-2">
          <span className="text-xs text-muted-foreground truncate">
            {listing.district}, {listing.city}
          </span>
          <div className="flex items-center gap-1">
            <span className={`h-2 w-2 rounded-full ${getStatusColor(listing.status)}`} />
            <span className="text-xs text-muted-foreground">{getStatusLabel(listing.status)}</span>
          </div>
        </div>
        <div className="flex items-center gap-1 pt-1">
          {canEdit && (
            <Button
              variant="outline"
              size="sm"
              className="h-7 text-xs"
              onClick={() => navigate(`/tin/${listing.id}/chinh-sua`)}
            >
              <Edit className="h-3 w-3 mr-1" />
              Sửa
            </Button>
          )}
          {canWithdraw && (
            <Button
              variant="outline"
              size="sm"
              className="h-7 text-xs"
              onClick={() => onWithdraw(listing.id)}
              disabled={isWithdrawing}
            >
              <ArrowLeftFromLine className="h-3 w-3 mr-1" />
              Rút
            </Button>
          )}
          {canDelete && (
            <Button
              variant="outline"
              size="sm"
              className="h-7 text-xs text-destructive hover:text-destructive"
              onClick={() => onDelete(listing.id)}
              disabled={isDeleting}
            >
              <Trash2 className="h-3 w-3 mr-1" />
              Xoá
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}

export function MyCartListingCardSkeleton() {
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
        <Skeleton className="h-7 w-16" />
      </div>
    </Card>
  )
}
