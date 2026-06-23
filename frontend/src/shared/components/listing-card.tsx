import { Link } from "react-router-dom"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { Heart, Ruler, DoorOpen, Bath, Building2 } from "lucide-react"

import { Card } from "@/shared/components/ui/card"
import { Badge } from "@/shared/components/ui/badge"
import { Skeleton } from "@/shared/components/ui/skeleton"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { formatPrice, formatDate, formatArea, getTransactionTypeLabel, getStatusLabel } from "@/shared/utils"
import type { IListing } from "@/shared/types/listing.type"

export function usePinListing() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, pinned }: { id: string; pinned: boolean }) =>
      pinned ? listingRepository.unpin(id) : listingRepository.pin(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.all })
    },
  })
}


export function ListingImageSection({
  listing,
  onTogglePin,
  isPinPending,
  showPinButton = true,
  actionMenu,
  children,
}: {
  listing: IListing
  onTogglePin: (e: React.MouseEvent) => void
  isPinPending: boolean
  showPinButton?: boolean
  actionMenu?: React.ReactNode
  children?: React.ReactNode
}) {
  return (
    <div className="relative aspect-[4/3] overflow-hidden bg-muted">
      {listing.primary_image_url ? (
        <img src={listing.primary_image_url} alt="" className="h-full w-full object-cover" />
      ) : (
        <div className="flex h-full w-full items-center justify-center text-xs text-muted-foreground">
          No Image
        </div>
      )}

      <div className="absolute top-2 left-2 rounded-full bg-white/90 px-2.5 py-1 text-xs font-bold text-red-600 shadow-sm">
        {formatPrice(listing.price, { compact: true })}
      </div>

      {(showPinButton || actionMenu) && (
        <div className="absolute top-2 right-2 flex items-center gap-1">
          {showPinButton && (
            <button
              type="button"
              onClick={onTogglePin}
              disabled={isPinPending}
              className="flex h-8 w-8 items-center justify-center rounded-full bg-white/80 shadow-sm hover:bg-white transition-colors disabled:opacity-50"
              aria-label={listing.is_pinned ? "Bỏ ghim" : "Ghim tin"}
            >
              <Heart
                className={`h-4 w-4 ${listing.is_pinned ? "fill-red-500 text-red-500" : "text-gray-600"}`}
              />
            </button>
          )}
          {actionMenu && (
            <div onClick={(e) => e.stopPropagation()}>
              {actionMenu}
            </div>
          )}
        </div>
      )}
      {children}
    </div>
  )
}

export function ListingStatusRow({ listing }: { listing: IListing }) {
  return (
    <div className="flex items-center gap-2">
      <Badge variant="outline" className="border-purple-500 text-purple-700 uppercase text-[10px] font-medium">
        {getTransactionTypeLabel(listing.transaction_type)}
      </Badge>
      <span className="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">
        {getStatusLabel(listing.status)}
      </span>
    </div>
  )
}

export function ListingTitle({ listing }: { listing: IListing }) {
  return (
    <p className="text-sm font-semibold leading-tight line-clamp-2">
      {listing.title || listing.address}
    </p>
  )
}

export function ListingLocation({ listing }: { listing: IListing }) {
  const parts = [listing.street_name, listing.ward, listing.district, listing.city].filter(Boolean)
  return (
    <p className="text-xs text-muted-foreground line-clamp-1">
      {parts.join(", ")}
    </p>
  )
}

export function ListingPricing({ listing }: { listing: IListing }) {
  const priceStr = formatPrice(listing.price)
  const areaStr = formatArea(listing.total_area)
  const perM2Str = listing.price_per_m2 ? ` = ${formatPrice(listing.price_per_m2)}/m²` : ""
  return (
    <div className="space-y-0.5">
      <p className="text-base font-bold text-destructive">
        {formatPrice(listing.price, { compact: true })}
      </p>
      <p className="text-xs text-muted-foreground">
        {priceStr} / {areaStr}{perM2Str}
      </p>
    </div>
  )
}

export function ListingDimensions({ listing }: { listing: IListing }) {
  return (
    <div className="flex items-center gap-1 text-xs text-muted-foreground">
      <Ruler className="h-3 w-3" />
      <span>{listing.area_width} x {listing.area_length} = {formatArea(listing.total_area)}</span>
    </div>
  )
}

export function ListingSpecs({ listing }: { listing: IListing }) {
  return (
    <div className="flex items-center gap-4 text-xs text-muted-foreground">
      {listing.num_rooms > 0 && (
        <span className="flex items-center gap-1">
          <DoorOpen className="h-3.5 w-3.5" />
          {listing.num_rooms} phòng
        </span>
      )}
      {listing.num_bathrooms > 0 && (
        <span className="flex items-center gap-1">
          <Bath className="h-3.5 w-3.5" />
          {listing.num_bathrooms} WC
        </span>
      )}
      {listing.num_floors > 0 && (
        <span className="flex items-center gap-1">
          <Building2 className="h-3.5 w-3.5" />
          {listing.num_floors} tầng
        </span>
      )}
    </div>
  )
}

export function ListingFooter({ listing }: { listing: IListing }) {
  return (
    <div className="border-t pt-2 mt-2 flex items-center justify-between text-[10px] text-muted-foreground">
      <span>{listing.creator?.full_name ?? "—"}</span>
      <span>{formatDate(listing.created_at)}</span>
    </div>
  )
}


export function ListingCard({
  listing,
  actionMenu,
  onClick,
}: {
  listing: IListing
  actionMenu?: React.ReactNode
  onClick?: () => void
}) {
  const pinMutation = usePinListing()

  const handleTogglePin = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    pinMutation.mutate({ id: listing.id, pinned: listing.is_pinned })
  }

  const content = (
    <>
      <ListingImageSection
        listing={listing}
        onTogglePin={handleTogglePin}
        isPinPending={pinMutation.isPending}
        actionMenu={actionMenu}
      />
      <div className="p-3 space-y-1.5">
        <ListingStatusRow listing={listing} />
        <ListingTitle listing={listing} />
        <ListingLocation listing={listing} />
        <ListingPricing listing={listing} />
        <ListingDimensions listing={listing} />
        <ListingSpecs listing={listing} />
        <ListingFooter listing={listing} />
      </div>
    </>
  )

  if (onClick) {
    return (
      <Card className="overflow-hidden p-0 gap-0 hover:shadow-md transition-shadow cursor-pointer" onClick={onClick}>
        {content}
      </Card>
    )
  }

  return (
    <Link to={`/tin/${listing.id}`} className="block group">
      <Card className="overflow-hidden p-0 gap-0 hover:shadow-md transition-shadow">
        {content}
      </Card>
    </Link>
  )
}

export function ListingCardSkeleton() {
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
      </div>
    </Card>
  )
}
