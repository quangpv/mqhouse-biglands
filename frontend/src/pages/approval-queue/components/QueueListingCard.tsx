import { Link } from "react-router-dom"
import { Card } from "@/shared/components/ui/card"
import { Badge } from "@/shared/components/ui/badge"
import { Checkbox } from "@/shared/components/ui/checkbox"
import { Button } from "@/shared/components/ui/button"
import { formatDate, formatPrice } from "@/shared/utils"
import type { IQueueItem } from "../types"
import { Check, X } from "lucide-react"

interface QueueListingCardProps {
  item: IQueueItem
  selected: boolean
  onSelect: () => void
  onApprove: () => void
  onReject: () => void
  showBulkSelect?: boolean
}

export function QueueListingCard({
  item,
  selected,
  onSelect,
  onApprove,
  onReject,
  showBulkSelect,
}: QueueListingCardProps) {
  const hasDealEvent = item.dealEvent && (item.dealEvent.customerName || item.dealEvent.notes)

  return (
    <Card className="p-4">
      <div className="flex gap-4">
        {showBulkSelect && (
          <div className="pt-1">
            <Checkbox checked={selected} onCheckedChange={onSelect} />
          </div>
        )}

        <div className="h-20 w-20 shrink-0 rounded-md overflow-hidden bg-muted">
          {item.listingImageUrl ? (
            <img src={item.listingImageUrl} alt="" className="h-full w-full object-cover" />
          ) : (
            <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
              No Image
            </div>
          )}
        </div>

        <div className="flex-1 min-w-0 space-y-1">
          <div className="flex items-start justify-between gap-2">
            <div>
              <Link
                to={`/tin/${item.listingId}`}
                className="font-semibold text-sm hover:underline line-clamp-1"
              >
                {item.listingTitle || item.listingCode}
              </Link>
              <p className="text-xs text-muted-foreground">Mã tin: {item.listingCode}</p>
            </div>
            <Badge variant="outline" className="shrink-0 text-[10px]">
              {item.listingStatus}
            </Badge>
          </div>

          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span>Người đăng: {item.agentName}</span>
            <span>Ngày: {formatDate(item.submittedAt)}</span>
          </div>

          {hasDealEvent && (
            <div className="rounded-md bg-muted/50 p-2 text-xs space-y-0.5">
              {item.dealEvent?.customerName && (
                <p>Khách: {item.dealEvent.customerName} ({item.dealEvent.customerPhone})</p>
              )}
              {item.dealEvent?.depositAmount && (
                <p>Tiền cọc: {formatPrice(item.dealEvent.depositAmount)}</p>
              )}
              {item.dealEvent?.notes && (
                <p className="italic">Ghi chú: {item.dealEvent.notes}</p>
              )}
            </div>
          )}

          {item.reporter && !hasDealEvent && (
            <p className="text-xs text-muted-foreground">
              Người báo cáo: {item.reporter.fullName}
            </p>
          )}

          <div className="flex gap-2 pt-1">
            <Button size="sm" variant="default" onClick={onApprove}>
              <Check className="h-3 w-3 mr-1" />
              Duyệt
            </Button>
            <Button size="sm" variant="outline" onClick={onReject}>
              <X className="h-3 w-3 mr-1" />
              Từ chối
            </Button>
          </div>
        </div>
      </div>
    </Card>
  )
}
