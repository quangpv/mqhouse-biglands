import type { ListingDTO, DealEventDTO } from "./listing.dto"

export interface ApprovalQueueItemDTO {
  id: string
  listing: ListingDTO
  approvalType: string
  dealEvent: DealEventDTO | null
  reportedBy: ReporterInfoDTO | null
  createdAt: string
}

export interface ReporterInfoDTO {
  id: string
  fullName: string
  username: string
  phone: string | null
}

export interface ApprovalQueuesResponseDTO {
  queues: Array<{
    queueType: string
    label: string
    transactionTypes: Array<{
      transactionType: string
      pendingCount: number
    }>
  }>
}

export interface ApprovalQueueItemListResponseDTO {
  data: ApprovalQueueItemDTO[]
  pagination: {
    page: number
    size: number
    totalItems: number
    totalPages: number
  }
}

export interface ApprovalDTO {
  id: string
  listingId: string
  approvalType: string
  decision: string
  decidedById: string
  reason: string | null
  createdAt: string
}

export interface BulkApproveResponseDTO {
  succeeded: string[]
  failed: Array<{
    id: string
    reason: string
  }>
}
