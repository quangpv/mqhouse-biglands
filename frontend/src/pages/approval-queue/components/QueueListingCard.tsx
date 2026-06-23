import { Check, X, MoreVertical } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/shared/components/ui/dropdown-menu"
import { Card } from "@/shared/components/ui/card"
import { Checkbox } from "@/shared/components/ui/checkbox"
import { ListingImageSection, ListingStatusRow, ListingTitle, ListingLocation, ListingPricing, ListingDimensions, ListingSpecs, usePinListing } from "@/shared/components/listing-card"
import { formatDate, formatPrice } from "@/shared/utils"
import type { IListing } from "@/shared/types/listing.type"

interface QueueDealEvent {
  customerName?: string
  customerPhone?: string
  depositAmount?: number
  notes?: string
}

interface QueueReporter {
  id: string
  fullName: string
}

interface QueueListingCardProps {
  listing: IListing
  selected: boolean
  onSelect: () => void
  onApprove: () => void
  onReject: () => void
  showBulkSelect?: boolean
  dealEvent?: QueueDealEvent | null
  reporter?: QueueReporter | null
}

export function QueueListingCard({
  listing,
  selected,
  onSelect,
  onApprove,
  onReject,
  showBulkSelect,
  dealEvent,
  reporter,
}: QueueListingCardProps) {
  const pinMutation = usePinListing()
  const hasDealEvent = dealEvent && (dealEvent.customerName || dealEvent.notes)

  const handleTogglePin = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    pinMutation.mutate({ id: listing.id, pinned: listing.is_pinned })
  }

  return (
    <Card className="overflow-hidden p-0 gap-0 hover:shadow-md transition-shadow">
      <ListingImageSection
        listing={listing}
        onTogglePin={handleTogglePin}
        isPinPending={pinMutation.isPending}
        actionMenu={
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button
                type="button"
                className="flex h-7 w-7 items-center justify-center rounded-full bg-white/80 shadow-sm hover:bg-white transition-colors"
                aria-label="Thao tác"
              >
                <MoreVertical className="h-4 w-4 text-gray-600" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="min-w-[140px]">
              <DropdownMenuItem onClick={onApprove}>
                <Check className="h-4 w-4 mr-2 text-green-600" />
                Duyệt
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onReject}>
                <X className="h-4 w-4 mr-2 text-red-600" />
                Từ chối
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        }
      >
        {showBulkSelect && (
          <div className="absolute bottom-2 left-2 z-10">
            <Checkbox
              checked={selected}
              onCheckedChange={onSelect}
              className="bg-white/80 shadow-sm data-[state=checked]:bg-white"
            />
          </div>
        )}
      </ListingImageSection>
      <div className="p-3 space-y-1.5">
        <ListingStatusRow listing={listing} />
        <ListingTitle listing={listing} />
        <ListingLocation listing={listing} />
        <ListingPricing listing={listing} />
        <ListingDimensions listing={listing} />
        <ListingSpecs listing={listing} />
        {listing.code && (
          <p className="text-xs text-muted-foreground">Mã tin: {listing.code}</p>
        )}
        {listing.creator && (
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span>Người đăng: {listing.creator.full_name}</span>
            <span>{formatDate(listing.created_at)}</span>
          </div>
        )}
        {hasDealEvent && (
          <div className="rounded-md bg-muted/50 p-2 text-xs space-y-0.5">
            {dealEvent?.customerName && (
              <p>Khách: {dealEvent.customerName} ({dealEvent.customerPhone})</p>
            )}
            {dealEvent?.depositAmount && (
              <p>Tiền cọc: {formatPrice(dealEvent.depositAmount)}</p>
            )}
            {dealEvent?.notes && (
              <p className="italic">Ghi chú: {dealEvent.notes}</p>
            )}
          </div>
        )}
        {reporter && !hasDealEvent && (
          <p className="text-xs text-muted-foreground">
            Người báo cáo: {reporter.fullName}
          </p>
        )}
      </div>
    </Card>
  )
}
