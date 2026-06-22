import { useState } from "react"
import { PageHeader } from "@/shared/components/page-header"
import { Button } from "@/shared/components/ui/button"
import { Separator } from "@/shared/components/ui/separator"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { Skeleton } from "@/shared/components/ui/skeleton"
import { HotProductList } from "./components/HotProductList"
import { AddHotProductDialog } from "./components/AddHotProductDialog"
import { useHotProductsState } from "./facades/useHotProductsState"
import { usePromoteToHot } from "./facades/usePromoteToHot"
import { useRemoveHot } from "./facades/useRemoveHot"
import { useReorderHot } from "./facades/useReorderHot"
import { Plus, Save, RotateCcw } from "lucide-react"

export default function HotProductsPage() {
  const {
    hotProducts,
    totalCount,
    isLoading,
    isError,
    refetch,
    moveUp,
    moveDown,
    isReordered,
    getCurrentOrder,
    resetOrder,
  } = useHotProductsState()

  const promote = usePromoteToHot()
  const remove = useRemoveHot()
  const reorder = useReorderHot()

  const [addDialogOpen, setAddDialogOpen] = useState(false)
  const [removeTarget, setRemoveTarget] = useState<string | null>(null)

  const handleAdd = (listingId: string) => {
    promote.mutate({ listingId, hotOrder: totalCount + 1 })
  }

  const handleRemove = (listingId: string) => {
    remove.mutate({ listingId })
  }

  const handleSaveOrder = () => {
    reorder.mutate(getCurrentOrder())
  }

  return (
    <div>
      <PageHeader
        title="Quản lý tin nổi bật"
        description={`${totalCount}/14 tin`}
        action={
          <div className="flex gap-2">
            {isReordered && (
              <>
                <Button variant="outline" size="sm" onClick={resetOrder}>
                  <RotateCcw className="h-4 w-4 mr-1" />
                  Hoàn tác
                </Button>
                <Button size="sm" onClick={handleSaveOrder} disabled={reorder.isPending}>
                  <Save className="h-4 w-4 mr-1" />
                  {reorder.isPending ? "Đang lưu..." : "Lưu thứ tự"}
                </Button>
              </>
            )}
            <Button onClick={() => setAddDialogOpen(true)} disabled={totalCount >= 14}>
              <Plus className="h-4 w-4 mr-1" />
              Thêm tin
            </Button>
          </div>
        }
      />

      <Separator className="mb-4" />

      {isLoading ? (
        <div className="space-y-2">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-20 w-full" />)}
        </div>
      ) : isError ? (
        <ErrorDisplay message="Không thể tải danh sách" onRetry={refetch} />
      ) : hotProducts.length === 0 ? (
        <EmptyState
          message="Chưa có tin nổi bật nào"
          actionLabel="Thêm tin"
          onAction={() => setAddDialogOpen(true)}
        />
      ) : (
        <HotProductList
          products={hotProducts}
          onMoveUp={moveUp}
          onMoveDown={moveDown}
          onRemove={handleRemove}
        />
      )}

      <AddHotProductDialog
        open={addDialogOpen}
        onOpenChange={setAddDialogOpen}
        onSelect={handleAdd}
        currentCount={totalCount}
      />
    </div>
  )
}
