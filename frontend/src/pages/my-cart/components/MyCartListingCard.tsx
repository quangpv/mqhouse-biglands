import { useNavigate } from "react-router-dom"
import { Card } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Skeleton } from "@/shared/components/ui/skeleton"
import { Edit, Trash2, ArrowLeftFromLine } from "lucide-react"
import {
  usePinListing,
  ListingImageSection,
  ListingStatusRow,
  ListingTitle,
  ListingLocation,
  ListingPricing,
  ListingDimensions,
  ListingSpecs,
} from "@/shared/components/listing-card"
import { formatDate } from "@/shared/utils"
import type { ListingDTO } from "@/data/types/listing.dto"

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
  const pinMutation = usePinListing()

  const canEdit = listing.status === "DRAFT" || listing.status === "CON_HANG"
  const canDelete = listing.status === "DRAFT"
  const canWithdraw = listing.status === "CON_HANG"

  const handleTogglePin = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    pinMutation.mutate({ id: listing.id, pinned: listing.is_pinned })
  }

  const handleCardClick = () => {
    navigate(`/tin/${listing.id}`)
  }

  return (
    <Card
      className="overflow-hidden p-0 gap-0 hover:shadow-md transition-shadow cursor-pointer"
      onClick={handleCardClick}
    >
      <ListingImageSection
        listing={listing}
        onTogglePin={handleTogglePin}
        isPinPending={pinMutation.isPending}
        showPinButton
      />
      <div className="p-3 space-y-1.5" onClick={(e) => e.stopPropagation()}>
        <ListingStatusRow listing={listing} />
        <ListingTitle listing={listing} />
        <ListingLocation listing={listing} />
        <ListingPricing listing={listing} />
        <ListingDimensions listing={listing} />
        <ListingSpecs listing={listing} />
        <div className="border-t pt-2 mt-2 flex items-center justify-between text-[10px] text-muted-foreground">
          <span>{listing.creator?.full_name ?? "—"}</span>
          <span>{formatDate(listing.created_at)}</span>
        </div>
      </div>
      {canEdit || canDelete || canWithdraw ? (
        <div className="px-3 pb-3 flex items-center gap-1">
          {canEdit && (
            <Button
              variant="outline"
              size="sm"
              className="h-7 text-xs"
              onClick={(e) => { e.stopPropagation(); navigate(`/tin/${listing.id}/chinh-sua`) }}
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
              onClick={(e) => { e.stopPropagation(); onWithdraw(listing.id) }}
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
              onClick={(e) => { e.stopPropagation(); onDelete(listing.id) }}
              disabled={isDeleting}
            >
              <Trash2 className="h-3 w-3 mr-1" />
              Xoá
            </Button>
          )}
        </div>
      ) : null}
    </Card>
  )
}

export function MyCartListingCardSkeleton() {
  return (
    <Card className="overflow-hidden p-0 gap-0">
      <Skeleton className="aspect-[4/3] w-full rounded-none" />
      <div className="p-3 space-y-2">
        <div className="flex gap-2">
          <Skeleton className="h-4 w-16 rounded-full" />
          <Skeleton className="h-4 w-14 rounded-full" />
        </div>
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-1/2" />
        <Skeleton className="h-5 w-1/3" />
        <Skeleton className="h-3 w-2/3" />
        <div className="flex gap-4">
          <Skeleton className="h-3 w-14" />
          <Skeleton className="h-3 w-14" />
          <Skeleton className="h-3 w-14" />
        </div>
        <div className="border-t pt-2 mt-2 flex justify-between">
          <Skeleton className="h-3 w-24" />
          <Skeleton className="h-3 w-16" />
        </div>
        <div className="flex gap-2 pt-1">
          <Skeleton className="h-7 w-12" />
          <Skeleton className="h-7 w-12" />
        </div>
      </div>
    </Card>
  )
}
