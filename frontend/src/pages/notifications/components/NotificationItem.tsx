import { useNavigate } from "react-router-dom"
import { Bell, CheckCheck } from "lucide-react"
import { Button } from "@/shared/components/ui/button"
import type { INotificationItem } from "../hooks/useNotificationMapper"

interface NotificationItemProps {
  notification: INotificationItem
  onMarkRead: (id: string) => void
}

const eventIcons: Record<string, string> = {
  listing_post_created: "📋",
  listing_post_approved: "✅",
  listing_post_rejected: "❌",
  deposit_reported: "💰",
  deposit_confirmed: "✅",
  deposit_rejected: "❌",
  closure_reported: "📝",
  closure_confirmed: "✅",
  closure_rejected: "❌",
  cancellation_reported: "🔄",
  cancellation_confirmed: "✅",
  cancellation_rejected: "❌",
  sold_out_reported: "🏷️",
  sold_out_confirmed: "✅",
  listing_expired: "⏰",
}

export function NotificationItem({ notification, onMarkRead }: NotificationItemProps) {
  const navigate = useNavigate()

  const handleClick = () => {
    if (!notification.isRead) {
      onMarkRead(notification.id)
    }
    if (notification.referenceId && notification.referenceType === "LISTING") {
      navigate(`/tin/${notification.referenceId}`)
    }
  }

  return (
    <div
      onClick={handleClick}
      className={`flex items-start gap-3 p-4 rounded-lg border cursor-pointer transition-colors hover:bg-accent ${
        !notification.isRead ? "bg-accent/30 border-primary/20" : ""
      }`}
    >
      <span className="text-lg mt-0.5">
        {eventIcons[notification.eventType ?? ""] || <Bell className="h-5 w-5 text-muted-foreground" />}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className={`text-sm ${!notification.isRead ? "font-semibold" : ""}`}>
            {notification.title}
          </p>
          <span className="text-xs text-muted-foreground whitespace-nowrap shrink-0">
            {notification.timeAgo}
          </span>
        </div>
        {notification.body && (
          <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{notification.body}</p>
        )}
      </div>
      {!notification.isRead && (
        <Button
          variant="ghost"
          size="icon"
          className="h-6 w-6 shrink-0"
          onClick={(e) => {
            e.stopPropagation()
            onMarkRead(notification.id)
          }}
        >
          <CheckCheck className="h-4 w-4 text-muted-foreground" />
        </Button>
      )}
    </div>
  )
}
