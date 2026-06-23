import { useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { useMyCartState } from "./facades/useMyCartState"
import { useDeleteListing } from "./facades/useDeleteListing"
import { useWithdrawListing } from "./facades/useWithdrawListing"
import { MyCartFilterTabs } from "./components/MyCartFilterTabs"
import { ListingCard, ListingCardSkeleton } from "@/shared/components/listing-card"
import { ListingActionDropdown } from "@/shared/components/listing-action-dropdown"
import { useAuthStore } from "@/shared/context/auth-store"
import { dtoToIListing } from "@/shared/mappers/listing.mapper"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { Plus } from "lucide-react"

export default function MyCartPage() {
  const { query, listings, tab, setTab, search, setSearch, statusTabs } = useMyCartState()
  const mappedListings = useMemo(() => listings.map(dtoToIListing), [listings])
  const { mutate: doDelete } = useDeleteListing()
  const { mutate: doWithdraw } = useWithdrawListing()
  const user = useAuthStore((s) => s.user)
  const navigate = useNavigate()

  return (
    <div>
      <PageHeader
        title="Giỏ hàng của tôi"
        description={query.data ? `${query.data.totalCount} tin` : undefined}
        action={
          <Button onClick={() => navigate("/tin/tao-moi")}>
            <Plus className="h-4 w-4 mr-1" />
            Nhập hàng mới
          </Button>
        }
      />

      <div className="mb-4 flex items-center gap-3">
        <Input
          placeholder="Tìm kiếm theo địa chỉ, mã tin..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value)
            setTab("all")
          }}
          className="max-w-sm"
        />
      </div>

      <MyCartFilterTabs tabs={statusTabs} active={tab} onTabChange={setTab} />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {query.isLoading ? (
          Array.from({ length: 8 }).map((_, i) => <ListingCardSkeleton key={i} />)
        ) : query.isError ? (
          <ErrorDisplay message="Không thể tải danh sách" onRetry={() => query.refetch()} />
        ) : listings.length === 0 ? (
          <EmptyState
            message="Không có tin nào"
            description={tab === "all" ? "Bạn chưa tạo tin đăng nào" : `Không có tin ở trạng thái này`}
            action={
              tab === "all" ? (
                <Button variant="outline" onClick={() => navigate("/tin/tao-moi")}>
                  Tạo tin đăng đầu tiên
                </Button>
              ) : undefined
            }
          />
        ) : (
          mappedListings.map((listing) => (
            <ListingCard
              key={listing.id}
              listing={listing}
              onClick={() => navigate(`/tin/${listing.id}`)}
              actionMenu={
                <ListingActionDropdown
                  listing={listing}
                  user={user}
                  onApprove={() => {}}
                  onReject={() => {}}
                  onEdit={(l) => navigate(`/tin/${l.id}/chinh-sua`)}
                  onDelete={(l) => doDelete(l.id)}
                  onWithdraw={(l) => doWithdraw(l.id)}
                  onBlockedAction={() => {}}
                  onPromoteToHot={() => {}}
                  onUnpromoteFromHot={() => {}}
                />
              }
            />
          ))
        )}
      </div>
    </div>
  )
}
