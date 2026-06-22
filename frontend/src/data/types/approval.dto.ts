import type { DealEventDTO } from "./listing.dto"

export interface ApprovalQueueItemDTO {
  id: string
  listing_id: string
  listing_code: string
  approval_type: string
  transaction_type: string
  title: string | null
  price: number | null
  status: string
  created_at: string
  customer_name: string | null
  customer_phone: string | null
  deposit_amount: number | null
  event_notes: string | null
  deal_event: DealEventInfoDTO | null
  reported_by: ReporterInfoDTO | null
}

export interface DealEventInfoDTO {
  event_type: string
  notes: string | null
  customer_name: string | null
  customer_phone: string | null
  deposit_amount: number | null
  created_at: string
}

export interface ReporterInfoDTO {
  id: string
  full_name: string | null
  email: string
}

export interface QueueCountDTO {
  approval_type: string
  transaction_type: string
  count: number
}

export interface ApprovalQueuesResponseDTO {
  queues: QueueCountDTO[]
}

export interface ApprovalQueueItemListResponseDTO {
  data: ApprovalQueueItemDTO[]
  page: number
  size: number
  total: number
  total_pages: number
}

export interface ApprovalDTO {
  id: string
  listing_id: string
  approval_type: string
  decision: string
  decided_by_id: string
  reason: string | null
  created_at: string
}

export interface BulkApproveResponseDTO {
  succeeded: string[]
  failed: Array<{
    id: string
    reason: string
  }>
}
