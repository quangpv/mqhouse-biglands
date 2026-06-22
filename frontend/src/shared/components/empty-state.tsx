import { Inbox } from "lucide-react"

interface EmptyStateProps {
  message?: string
  description?: string
  action?: React.ReactNode
}

export function EmptyState({ message = "Không có dữ liệu", description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-2">
      <Inbox className="h-12 w-12 text-muted-foreground" />
      <p className="font-medium">{message}</p>
      {description && <p className="text-sm text-muted-foreground">{description}</p>}
      {action}
    </div>
  )
}
