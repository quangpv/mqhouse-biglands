import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { notificationRepository } from "@/data/repositories/notification.repository"
import { notificationQueries } from "@/data/queries/notification.queries"
import type { NotificationFilter } from "../types"

export function useNotificationState() {
  const [filter, setFilter] = useState<NotificationFilter>("all")
  const [page, setPage] = useState(1)

  const listQuery = useQuery({
    queryKey: notificationQueries.list({ filter, page }),
    queryFn: () => notificationRepository.list({ page, size: 20, is_read: filter === "unread" ? false : undefined }),
  })

  const unreadQuery = useQuery({
    queryKey: notificationQueries.unreadCount(),
    queryFn: () => notificationRepository.getUnreadCount(),
  })

  const notifications = listQuery.data?.data ?? []
  const unreadCount = unreadQuery.data?.count ?? 0

  const filterTabs: Array<{ key: NotificationFilter; label: string }> = [
    { key: "all", label: "Tất cả" },
    { key: "unread", label: `Chưa đọc${unreadCount > 0 ? ` (${unreadCount})` : ""}` },
  ]

  return { listQuery, unreadCount, notifications, filter, setFilter, page, setPage, filterTabs }
}
