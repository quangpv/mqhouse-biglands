import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
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
import { ChevronLeft, ChevronRight } from "lucide-react"

export default function QueueListPage() {
  const { queueType } = useParams<{ queueType: string }>()
  const navigate = useNavigate()
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

  const mappedItems = items.map((item) => ({
    id: item.id,
    listingId: item.listing_id,
    listingTitle: item.title ?? "",
    listingCode: item.listing_code ?? "",
    listingImageUrl: null,
    listingStatus: item.status ?? "",
    approvalType: typedQueueType,
    agentName: item.reported_by?.full_name ?? "",
    submittedAt: item.created_at,
    dealEvent: item.deal_event
      ? {
          customerName: item.deal_event.customer_name,
          customerPhone: item.deal_event.customer_phone,
          depositAmount: item.deal_event.deposit_amount,
          notes: item.deal_event.notes,
        }
      : null,
    reporter: item.reported_by
      ? { id: item.reported_by.id, fullName: item.reported_by.full_name }
      : null,
  }))

  return (
    <div>
      <QueueHeader title={getQueueTitle(typedQueueType)} pendingCount={pendingCount} />

      <div className="space-y-3">
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
                item={item}
                selected={selectedIds.has(item.id)}
                onSelect={() => toggleSelect(item.id)}
                onApprove={() => setApproveTarget(item.id)}
                onReject={() => setRejectTarget(item.id)}
                showBulkSelect={isListingPost}
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
  const { queueType, id } = useParams<{ queueType: string; id: string }>()
  const navigate = useNavigate()
  const typedQueueType = (queueType ?? "listing-post") as QueueType

  const itemQuery = useQuery({
    queryKey: approvalQueries.detail(id ?? ""),
    queryFn: () => approvalRepository.get(id ?? ""),
    enabled: !!id,
  })

  return (
    <div>
      <QueueHeader title={`${getQueueTitle(typedQueueType)} — Chi tiết`} />
    </div>
  )
}
