import httpClient from "../infra/http-client"
import type { ApprovalQueuesResponseDTO, ApprovalQueueItemListResponseDTO, ApprovalDTO, BulkApproveResponseDTO } from "../types/approval.dto"

export interface QueueItemListParams {
  transactionType?: string
  page?: number
  size?: number
  dateFrom?: string
  dateTo?: string
  agentId?: string
}

export const approvalRepository = {
  getQueues: () =>
    httpClient.get<ApprovalQueuesResponseDTO>("/approvals/queues").then((r) => r.data),

  listQueueItems: (queueType: string, params?: QueueItemListParams) =>
    httpClient.get<ApprovalQueueItemListResponseDTO>(`/approvals/queues/${queueType}`, { params }).then((r) => r.data),

  get: (id: string) =>
    httpClient.get<ApprovalDTO>(`/approvals/${id}`).then((r) => r.data),

  approve: (id: string) =>
    httpClient.post<ApprovalDTO>(`/approvals/${id}/approve`).then((r) => r.data),

  reject: (id: string, reason: string) =>
    httpClient.post<ApprovalDTO>(`/approvals/${id}/reject`, { reason }).then((r) => r.data),

  bulkApprove: (ids: string[]) =>
    httpClient.post<BulkApproveResponseDTO>("/approvals/bulk-approve", { ids }).then((r) => r.data),
}
