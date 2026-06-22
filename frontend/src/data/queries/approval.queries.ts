export const approvalQueries = {
  all: ["approvals"] as const,
  queues: () => [...approvalQueries.all, "queues"] as const,
  queueList: (type: string, params: Record<string, unknown>) =>
    [...approvalQueries.queues(), type, params] as const,
  detail: (id: string) => [...approvalQueries.all, "detail", id] as const,
}
