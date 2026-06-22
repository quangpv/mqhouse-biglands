import { Button } from "@/shared/components/ui/button"
import { AlertCircle } from "lucide-react"

interface ErrorDisplayProps {
  message?: string
  onRetry?: () => void
}

export function ErrorDisplay({ message = "Đã có lỗi xảy ra", onRetry }: ErrorDisplayProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <AlertCircle className="h-12 w-12 text-destructive" />
      <p className="text-muted-foreground">{message}</p>
      {onRetry && <Button variant="outline" onClick={onRetry}>Thử lại</Button>}
    </div>
  )
}
