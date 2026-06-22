import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/shared/components/ui/tabs"
import { Badge } from "@/shared/components/ui/badge"
import { Card } from "@/shared/components/ui/card"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { ListingCard, ListingCardSkeleton } from "./components/ListingCard"
import { Plus, ChevronLeft, ChevronRight, Flame } from "lucide-react"
import { formatPrice } from "@/shared/utils"

type FilterTab = "all" | "hot" | "pinned"

export default function SharedCartPage() {
  const navigate = useNavigate()
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

  const hotStripQuery = useQuery({
    queryKey: listingQueries.hotStrip(),
    queryFn: () => listingRepository.getHotListings({ page: 1, size: 14 }),
  })

  const activeQuery = tab === "all" ? allQuery : tab === "hot" ? hotQuery : pinnedQuery
  const listings = activeQuery.data?.data ?? []
  const filterCounts = allQuery.data?.filterCounts
  const totalCount = allQuery.data?.totalCount ?? 0
  const pagination = allQuery.data?.pagination
  const totalPages = pagination?.totalPages ?? 1

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

      {hotStripQuery.data && hotStripQuery.data.data.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold mb-2 flex items-center gap-1">
            <Flame className="h-4 w-4 text-red-500" />
            Hàng Hot
          </h3>
          <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin">
            {hotStripQuery.data.data.map((listing) => (
              <Link
                key={listing.id}
                to={`/tin/${listing.id}`}
                className="shrink-0 w-44 group"
              >
                <Card className="overflow-hidden">
                  <div className="relative h-28 bg-muted">
                    {listing.primaryImageUrl ? (
                      <img src={listing.primaryImageUrl} alt="" className="h-full w-full object-cover" />
                    ) : (
                      <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
                        No Image
                      </div>
                    )}
                    <Badge className="absolute top-1 left-1 bg-red-500 text-white text-[10px] px-1.5 py-0">
                      Hot
                    </Badge>
                  </div>
                  <div className="p-2 space-y-1">
                    <p className="text-xs font-semibold truncate group-hover:underline">
                      {listing.title || listing.address}
                    </p>
                    <p className="text-sm font-bold text-primary">
                      {formatPrice(listing.price, { compact: true })}
                    </p>
                    <p className="text-[10px] text-muted-foreground truncate">
                      {listing.district}
                    </p>
                  </div>
                </Card>
              </Link>
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
          <>
            {listings.map((listing) => <ListingCard key={listing.id} listing={listing} />)}
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
    </div>
  )
}
