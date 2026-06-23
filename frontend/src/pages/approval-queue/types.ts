export type QueueType = "listing-post" | "deposit" | "closure" | "cancellation" | "sold-out"

export type TransactionType = "BAN" | "CHO_THUE" | "SANG_NHUONG"

export interface QueueFilterState {
  date_from: string
  date_to: string
  agent_id: string
}

export interface IRejectForm {
  reason: string
}
