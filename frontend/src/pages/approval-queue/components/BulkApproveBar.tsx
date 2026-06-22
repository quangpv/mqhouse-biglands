import { Button } from "@/shared/components/ui/button"
import { Check } from "lucide-react"

interface BulkApproveBarProps {
  selectedCount: number
  onApproveAll: () => void
  onClear: () => void
  isPending: boolean
}

export function BulkApproveBar({
  selectedCount,
  onApproveAll,
  onClear,
  isPending,
}: BulkApproveBarProps) {
  if (selectedCount === 0) return null

  return (
    <div className="sticky bottom-4 z-10 flex items-center justify-between rounded-lg border bg-background px-4 py-3 shadow-lg">
      <span className="text-sm font-medium">
        Đã chọn {selectedCount} yêu cầu
      </span>
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={onClear}>
          Bỏ chọn
        </Button>
        <Button size="sm" onClick={onApproveAll} disabled={isPending}>
          <Check className="h-4 w-4 mr-1" />
          {isPending ? "Đang duyệt..." : "Duyệt tất cả"}
        </Button>
      </div>
    </div>
  )
}
