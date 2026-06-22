import httpClient from "../infra/http-client"
import type { ApprovalQueuesResponseDTO, ApprovalQueueItemListResponseDTO, ApprovalDTO, BulkApproveResponseDTO } from "../types/approval.dto"

export interface QueueItemListParams {
  transaction_type?: string
  page?: number
  size?: number
  date_from?: string
  date_to?: string
  agent_id?: string
}

const QUEUE_TYPE_TO_BACKEND: Record<string, string> = {
  "listing-post": "LISTING_POST",
  deposit: "DEPOSIT",
  closure: "CLOSURE",
  cancellation: "CANCELLATION",
  "sold-out": "SOLD_OUT",
}

export const approvalRepository = {
  getQueues: () =>
    httpClient.get<ApprovalQueuesResponseDTO>("/approvals/queues").then((r) => r.data),

  listQueueItems: (queueType: string, params?: QueueItemListParams) => {
    const backendType = QUEUE_TYPE_TO_BACKEND[queueType] ?? queueType.toUpperCase()
    return httpClient.get<ApprovalQueueItemListResponseDTO>(`/approvals/queues/${backendType}`, { params }).then((r) => r.data)
  },

  get: (id: string) =>
    httpClient.get<ApprovalDTO>(`/approvals/${id}`).then((r) => r.data),

  approve: (id: string) =>
    httpClient.post<ApprovalDTO>(`/approvals/${id}/approve`).then((r) => r.data),

  reject: (id: string, reason: string) =>
    httpClient.post<ApprovalDTO>(`/approvals/${id}/reject`, { reason }).then((r) => r.data),

  bulkApprove: (ids: string[]) =>
    httpClient.post<BulkApproveResponseDTO>("/approvals/bulk-approve", { ids }).then((r) => r.data),
}
