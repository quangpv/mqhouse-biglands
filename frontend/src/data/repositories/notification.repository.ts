import httpClient from "../infra/http-client"
import type { NotificationListResponseDTO, NotificationDTO } from "../types/notification.dto"

export interface NotificationListParams {
  page?: number
  size?: number
  isRead?: boolean
  transactionType?: string
  q?: string
}

export const notificationRepository = {
  list: (params?: NotificationListParams) =>
    httpClient.get<NotificationListResponseDTO>("/notifications", { params }).then((r) => r.data),

  getUnreadCount: () =>
    httpClient.get<{ count: number }>("/notifications/unread-count").then((r) => r.data),

  markRead: (id: string) =>
    httpClient.patch<NotificationDTO>(`/notifications/${id}/read`).then((r) => r.data),

  markAllRead: () =>
    httpClient.post<{ updated: number }>("/notifications/read-all").then((r) => r.data),

  getPreferences: () =>
    httpClient.get("/users/me/notification-preferences").then((r) => r.data),

  updatePreferences: (data: Record<string, boolean>) =>
    httpClient.put("/users/me/notification-preferences", data).then((r) => r.data),
}
