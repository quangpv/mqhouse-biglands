import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Tabs, TabsList, TabsTrigger } from "@/shared/components/ui/tabs"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { ListingCard, ListingCardSkeleton } from "./components/ListingCard"

type FilterTab = "all" | "hot" | "pinned"

export default function SharedCartPage() {
  const [tab, setTab] = useState<FilterTab>("all")
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)

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

  const activeQuery = tab === "all" ? allQuery : tab === "hot" ? hotQuery : pinnedQuery
  const listings = activeQuery.data?.data ?? []
  const filterCounts = allQuery.data?.filterCounts
  const totalCount = allQuery.data?.totalCount ?? 0

  return (
    <div>
      <PageHeader
        title="Giỏ hàng chung"
        description={`${totalCount} tin đang bán`}
      />

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

      <div className="space-y-3">
        {activeQuery.isLoading ? (
          Array.from({ length: 6 }).map((_, i) => <ListingCardSkeleton key={i} />)
        ) : activeQuery.isError ? (
          <ErrorDisplay message="Không thể tải danh sách" onRetry={() => activeQuery.refetch()} />
        ) : listings.length === 0 ? (
          <EmptyState
            message="Không có tin nào"
            description={tab === "pinned" ? "Bạn chưa ghim tin nào" : "Không tìm thấy kết quả phù hợp"}
          />
        ) : (
          listings.map((listing) => <ListingCard key={listing.id} listing={listing} />)
        )}
      </div>
    </div>
  )
}
