import { useState, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/shared/components/ui/tabs"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { ListingCard, ListingCardSkeleton } from "@/shared/components/listing-card"
import { ListingActionDropdown } from "@/shared/components/listing-action-dropdown"
import { BlockedActionDialog } from "@/shared/components/blocked-action-dialog"
import { ApproveConfirmDialog } from "@/pages/approval-queue/components/ApproveConfirmDialog"
import { RejectReasonDialog } from "@/pages/approval-queue/components/RejectReasonDialog"
import { useAuthStore } from "@/shared/context/auth-store"
import { useHomeListingActions } from "./facades/useHomeListingActions"
import { dtoToIListing } from "@/shared/mappers/listing.mapper"
import { Plus, ChevronLeft, ChevronRight, Flame } from "lucide-react"

type FilterTab = "all" | "hot" | "pinned"

export default function SharedCartPage() {
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const [tab, setTab] = useState<FilterTab>("all")
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)

  const {
    actionDialog,
    closeDialog,
    handleApprove,
    handleReject,
    handleEdit,
    handleDelete,
    handleBlockedAction,
    handlePromoteToHot,
    handleUnpromoteFromHot,
    confirmApprove,
    confirmReject,
    isApproving,
    isRejecting,
  } = useHomeListingActions()

  const allQuery = useQuery({
    queryKey: listingQueries.list({ tab: "all", search, page }),
    queryFn: () => listingRepository.list({ q: search || undefined, page, size: 20 }),
  })

  const hotQuery = useQuery({
    queryKey: listingQueries.hot(),
    queryFn: () => listingRepository.getHotListings({ page: 1, size: 50 }),
    enabled: tab === "hot",
  })

  const pinnedQuery = useQuery({
    queryKey: listingQueries.pins(),
    queryFn: () => listingRepository.getMyPins({ page: 1, size: 50 }),
    enabled: tab === "pinned",
  })

  const hotStripQuery = useQuery({
    queryKey: listingQueries.hotStrip(),
    queryFn: () => listingRepository.getHotListings({ page: 1, size: 14 }),
  })

  const activeQuery = tab === "all" ? allQuery : tab === "hot" ? hotQuery : pinnedQuery
  const listings = activeQuery.data?.data ?? []
  const mappedListings = useMemo(() => listings.map(dtoToIListing), [listings])
  const hotStripListings = useMemo(
    () => (hotStripQuery.data?.data ?? []).map(dtoToIListing),
    [hotStripQuery.data]
  )
  const filterCountsQuery = useQuery({
    queryKey: listingQueries.filterCounts(),
    queryFn: () => listingRepository.getFilterCounts(),
  })
  const filterCounts = filterCountsQuery.data
  const totalCount = allQuery.data?.total_count ?? 0
  const totalPages = allQuery.data?.total_pages ?? 1

  return (
    <div>
      <PageHeader
        title="Giỏ hàng chung"
        description={`${totalCount} tin đang bán`}
        action={
          <Button onClick={() => navigate("/tin/tao-moi")}>
            <Plus className="h-4 w-4 mr-1" />
            Nhập hàng mới
          </Button>
        }
      />

      {hotStripListings.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold mb-2 flex items-center gap-1">
            <Flame className="h-4 w-4 text-red-500" />
            Hàng Hot
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {hotStripListings.map((listing) => (
              <ListingCard key={listing.id} listing={listing} />
            ))}
          </div>
        </div>
      )}

      <div className="mb-4 flex items-center gap-3">
        <Input
          placeholder="Tìm kiếm theo địa chỉ, mã tin..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); setTab("all") }}
          className="max-w-sm"
        />
      </div>

      <Tabs value={tab} onValueChange={(v) => { setTab(v as FilterTab); setPage(1) }}>
        <TabsList className="mb-4">
          <TabsTrigger value="all">
            Tất cả {filterCounts ? `(${filterCounts.all})` : ""}
          </TabsTrigger>
          <TabsTrigger value="hot">
            Hàng Hot {filterCounts ? `(${filterCounts.hot})` : ""}
          </TabsTrigger>
          <TabsTrigger value="pinned">
            Đã ghim {filterCounts ? `(${filterCounts.pinned})` : ""}
          </TabsTrigger>
        </TabsList>
      </Tabs>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {activeQuery.isLoading ? (
          Array.from({ length: 8 }).map((_, i) => <ListingCardSkeleton key={i} />)
        ) : activeQuery.isError ? (
          <ErrorDisplay message="Không thể tải danh sách" onRetry={() => activeQuery.refetch()} />
        ) : listings.length === 0 ? (
          <EmptyState
            message="Không có tin nào"
            description={tab === "pinned" ? "Bạn chưa ghim tin nào" : "Không tìm thấy kết quả phù hợp"}
          />
        ) : (
          <>
            {mappedListings.map((listing) => (
              <ListingCard
                key={listing.id}
                listing={listing}
                actionMenu={
                  <ListingActionDropdown
                    listing={listing}
                    user={user}
                    onApprove={handleApprove}
                    onReject={handleReject}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onBlockedAction={handleBlockedAction}
                    onPromoteToHot={handlePromoteToHot}
                    onUnpromoteFromHot={handleUnpromoteFromHot}
                  />
                }
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

      <ApproveConfirmDialog
        open={actionDialog?.type === "approve"}
        onOpenChange={(open) => { if (!open) closeDialog() }}
        onConfirm={confirmApprove}
        isPending={isApproving}
      />

      <RejectReasonDialog
        open={actionDialog?.type === "reject"}
        onOpenChange={(open) => { if (!open) closeDialog() }}
        onConfirm={confirmReject}
        isPending={isRejecting}
      />

      <BlockedActionDialog
        open={actionDialog?.type === "blocked-edit" || actionDialog?.type === "blocked-delete"}
        onOpenChange={(open) => { if (!open) closeDialog() }}
        status={actionDialog?.listing.status ?? ""}
        actionLabel={actionDialog?.type === "blocked-edit" ? "sửa" : "xoá"}
      />
    </div>
  )
}
