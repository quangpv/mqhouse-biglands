import { Button } from "@/shared/components/ui/button"
import { MessageSquare } from "lucide-react"

export function ReviewsSection() {
  return (
    <div className="space-y-4">
      <h3 className="font-semibold">Nhận xét & Đánh giá</h3>
      <div className="flex flex-col items-center justify-center gap-2 rounded-lg border py-10 text-center">
        <MessageSquare className="h-8 w-8 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">Chưa có nhận xét nào</p>
        <p className="text-xs text-muted-foreground">Tính năng đang phát triển</p>
        <Button variant="outline" size="sm" disabled>
          Gửi đánh giá
        </Button>
      </div>
    </div>
  )
}
