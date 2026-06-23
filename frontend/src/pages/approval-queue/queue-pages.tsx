import { useState, useMemo } from "react"
import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import { Button } from "@/shared/components/ui/button"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { ListingCardSkeleton } from "@/shared/components/listing-card"
import { QueueHeader } from "./components/QueueHeader"
import { QueueListingCard } from "./components/QueueListingCard"
import { ApproveConfirmDialog } from "./components/ApproveConfirmDialog"
import { RejectReasonDialog } from "./components/RejectReasonDialog"
import { BulkApproveBar } from "./components/BulkApproveBar"
import { useApproveItem } from "./facades/useApproveItem"
import { useRejectItem } from "./facades/useRejectItem"
import { useBulkApprove } from "./facades/useBulkApprove"
import { getQueueTitle } from "./constants/queueUI"
import type { QueueType } from "./types"
import type { IListing } from "@/shared/types/listing.type"
import { ChevronLeft, ChevronRight } from "lucide-react"

export default function QueueListPage() {
  const { queueType } = useParams<{ queueType: string }>()
  const [page, setPage] = useState(1)
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [approveTarget, setApproveTarget] = useState<string | null>(null)
  const [rejectTarget, setRejectTarget] = useState<string | null>(null)

  const typedQueueType = (queueType ?? "listing-post") as QueueType

  const queuesQuery = useQuery({
    queryKey: approvalQueries.queues(),
    queryFn: () => approvalRepository.getQueues(),
  })

  const itemsQuery = useQuery({
    queryKey: approvalQueries.queueList(typedQueueType, { page }),
    queryFn: () => approvalRepository.listQueueItems(typedQueueType, { page, size: 20 }),
  })

  const approveItem = useApproveItem()
  const rejectItem = useRejectItem()
  const bulkApprove = useBulkApprove()

  const QUEUE_TYPE_MAP: Record<string, string> = {
    "listing-post": "LISTING_POST",
    deposit: "DEPOSIT",
    closure: "CLOSURE",
    cancellation: "CANCELLATION",
    "sold-out": "SOLD_OUT",
  }
  const backendType = QUEUE_TYPE_MAP[typedQueueType] ?? typedQueueType.toUpperCase()
  const currentQueue = queuesQuery.data?.queues.filter((q) => q.approval_type === backendType) ?? []
  const pendingCount = currentQueue.reduce((s, q) => s + q.count, 0)
  const items = itemsQuery.data?.data ?? []
  const totalPages = itemsQuery.data?.total_pages ?? 1
  const isListingPost = typedQueueType === "listing-post"

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const clearSelection = () => setSelectedIds(new Set())

  const handleBulkApprove = () => {
    bulkApprove.mutate(
      { ids: Array.from(selectedIds) },
      { onSuccess: () => setSelectedIds(new Set()) }
    )
  }

  const mappedItems = useMemo(() => items.map((item) => {
    const listing: IListing = {
      id: item.listing_id,
      code: item.listing_code,
      transaction_type: item.transaction_type,
      title: item.title,
      price: item.price ?? 0,
      total_area: item.total_area ?? 0,
      price_per_m2: item.price_per_m2,
      area_width: item.area_width ?? 0,
      area_length: item.area_length ?? 0,
      num_rooms: item.num_rooms,
      num_bathrooms: item.num_bathrooms,
      num_floors: item.num_floors,
      street_name: item.street_name,
      ward: item.ward,
      district: item.district,
      city: item.city,
      address: item.address,
      status: item.status,
      is_hot: item.is_hot,
      is_pinned: item.is_pinned,
      hot_order: item.hot_order,
      primary_image_url: item.primary_image_url,
      created_by_id: item.created_by_id ?? "",
      creator: item.creator_name ? { full_name: item.creator_name } : null,
      created_at: item.listing_created_at ?? item.created_at,
    }
    return {
      id: item.id,
      listing,
      dealEvent: item.deal_event
        ? {
            customerName: item.deal_event.customer_name ?? undefined,
            customerPhone: item.deal_event.customer_phone ?? undefined,
            depositAmount: item.deal_event.deposit_amount ?? undefined,
            notes: item.deal_event.notes ?? undefined,
          }
        : null,
      reporter: item.reported_by
        ? { id: item.reported_by.id, fullName: item.reported_by.full_name ?? "" }
        : null,
    }
  }), [items])

  return (
    <div>
      <QueueHeader title={getQueueTitle(typedQueueType)} pendingCount={pendingCount} />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {itemsQuery.isLoading ? (
          Array.from({ length: 5 }).map((_, i) => <ListingCardSkeleton key={i} />)
        ) : itemsQuery.isError ? (
          <ErrorDisplay message="Không thể tải danh sách" onRetry={() => itemsQuery.refetch()} />
        ) : mappedItems.length === 0 ? (
          <EmptyState
            message="Không có yêu cầu nào"
            description="Tất cả yêu cầu đã được xử lý"
          />
        ) : (
          <>
            {mappedItems.map((item) => (
              <QueueListingCard
                key={item.id}
                listing={item.listing}
                selected={selectedIds.has(item.id)}
                onSelect={() => toggleSelect(item.id)}
                onApprove={() => setApproveTarget(item.id)}
                onReject={() => setRejectTarget(item.id)}
                showBulkSelect={isListingPost}
                dealEvent={item.dealEvent}
                reporter={item.reporter}
              />
            ))}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 pt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page <= 1}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter((p) => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                  .map((p, idx, arr) => (
                    <span key={p} className="flex items-center">
                      {idx > 0 && arr[idx - 1] !== p - 1 && (
                        <span className="px-1 text-muted-foreground">...</span>
                      )}
                      <Button
                        variant={page === p ? "default" : "outline"}
                        size="sm"
                        className="min-w-[36px]"
                        onClick={() => setPage(p)}
                      >
                        {p}
                      </Button>
                    </span>
                  ))}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page >= totalPages}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            )}
          </>
        )}
      </div>

      {isListingPost && (
        <BulkApproveBar
          selectedCount={selectedIds.size}
          onApproveAll={handleBulkApprove}
          onClear={clearSelection}
          isPending={bulkApprove.isPending}
        />
      )}

      <ApproveConfirmDialog
        open={!!approveTarget}
        onOpenChange={(open) => { if (!open) setApproveTarget(null) }}
        onConfirm={(reason) => {
          if (approveTarget) {
            approveItem.mutate({ id: approveTarget })
            setApproveTarget(null)
          }
        }}
        isPending={approveItem.isPending}
      />

      <RejectReasonDialog
        open={!!rejectTarget}
        onOpenChange={(open) => { if (!open) setRejectTarget(null) }}
        onConfirm={(reason) => {
          if (rejectTarget) {
            rejectItem.mutate({ id: rejectTarget, reason })
            setRejectTarget(null)
          }
        }}
        isPending={rejectItem.isPending}
      />
    </div>
  )
}

export function QueueDetailPage() {
  const { queueType } = useParams<{ queueType: string }>()
  const typedQueueType = (queueType ?? "listing-post") as QueueType

  return (
    <div>
      <QueueHeader title={`${getQueueTitle(typedQueueType)} — Chi tiết`} />
    </div>
  )
}
