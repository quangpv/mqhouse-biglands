import { useMyCartState } from "./facades/useMyCartState"
import { useDeleteListing } from "./facades/useDeleteListing"
import { useWithdrawListing } from "./facades/useWithdrawListing"
import { MyCartFilterTabs } from "./components/MyCartFilterTabs"
import { MyCartListingCard, MyCartListingCardSkeleton } from "./components/MyCartListingCard"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { Plus } from "lucide-react"
import { useNavigate } from "react-router-dom"

export default function MyCartPage() {
  const { query, listings, tab, setTab, search, setSearch, statusTabs } = useMyCartState()
  const { mutate: doDelete, isPending: isDeleting } = useDeleteListing()
  const { mutate: doWithdraw, isPending: isWithdrawing } = useWithdrawListing()
  const navigate = useNavigate()

  return (
    <div>
      <PageHeader
        title="Giỏ hàng chung"
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

      <div className="space-y-3">
        {query.isLoading ? (
          Array.from({ length: 6 }).map((_, i) => <MyCartListingCardSkeleton key={i} />)
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
          listings.map((listing) => (
            <MyCartListingCard
              key={listing.id}
              listing={listing}
              onDelete={doDelete}
              onWithdraw={doWithdraw}
              isDeleting={isDeleting}
              isWithdrawing={isWithdrawing}
            />
          ))
        )}
      </div>
    </div>
  )
}
