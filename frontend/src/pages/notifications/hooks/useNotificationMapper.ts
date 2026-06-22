import type { NotificationDTO } from "@/data/types/notification.dto"

export interface INotificationItem {
  id: string
  title: string
  body: string
  eventType: string | null
  actorName: string | null
  transactionType: string | null
  referenceType: string | null
  referenceId: string | null
  isRead: boolean
  timeAgo: string
  createdAt: string
}

export function useNotificationMapper() {
  function toUI(dto: NotificationDTO): INotificationItem {
    return {
      id: dto.id,
      title: dto.title,
      body: dto.body,
      eventType: dto.event_type,
      actorName: dto.actor_name,
      transactionType: dto.transaction_type,
      referenceType: dto.reference_type,
      referenceId: dto.reference_id,
      isRead: dto.is_read,
      createdAt: dto.created_at,
      timeAgo: getRelativeTime(dto.created_at),
    }
  }

  return { toUI }
}

function getRelativeTime(dateStr: string): string {
  const now = Date.now()
  const then = new Date(dateStr).getTime()
  const diffMs = now - then
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffSec < 10) return "Vừa xong"
  if (diffSec < 60) return `${diffSec} giây trước`
  if (diffMin < 60) return `${diffMin} phút trước`
  if (diffHour < 24) return `${diffHour} giờ trước`
  if (diffDay < 7) return `${diffDay} ngày trước`
  return new Date(dateStr).toLocaleDateString("vi-VN")
}
