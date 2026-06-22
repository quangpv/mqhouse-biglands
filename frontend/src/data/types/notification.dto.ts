export interface NotificationDTO {
  id: string
  user_id: string
  title: string
  body: string
  event_type: string | null
  actor_name: string | null
  transaction_type: string | null
  reference_type: string | null
  reference_id: string | null
  is_read: boolean
  created_at: string
}

export interface NotificationListResponseDTO {
  data: NotificationDTO[]
  page: number
  size: number
  total: number
  total_pages: number
  unread_count: number
  category_counts: Record<string, number>
}
