export interface NotificationDTO {
  id: string
  userId: string
  title: string
  body: string
  eventType: string | null
  actorName: string | null
  transactionType: string | null
  referenceType: string | null
  referenceId: string | null
  isRead: boolean
  createdAt: string
}

export interface NotificationListResponseDTO {
  data: NotificationDTO[]
  pagination: {
    page: number
    size: number
    totalItems: number
    totalPages: number
  }
  unreadCount: number
  categoryCounts: Record<string, number>
}
