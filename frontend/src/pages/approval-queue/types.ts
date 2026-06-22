export type QueueType = "listing-post" | "deposit" | "closure" | "cancellation" | "sold-out"

export type TransactionType = "BAN" | "CHO_THUE" | "SANG_NHUONG"

export interface QueueFilterState {
  dateFrom: string
  dateTo: string
  agentId: string
}

export interface IQueueItem {
  id: string
  listingId: string
  listingTitle: string
  listingCode: string
  listingImageUrl: string | null
  listingStatus: string
  approvalType: QueueType
  agentName: string
  submittedAt: string
  dealEvent: {
    customerName?: string
    customerPhone?: string
    depositAmount?: number
    notes?: string
  } | null
  reporter: {
    id: string
    fullName: string
  } | null
}

export interface IRejectForm {
  reason: string
}
