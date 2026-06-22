import { useState, useMemo } from "react"
import { useQuery } from "@tanstack/react-query"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import type { QueueType, QueueFilterState } from "../types"

const QUEUE_TYPE_MAP: Record<QueueType, string> = {
  "listing-post": "LISTING_POST",
  deposit: "DEPOSIT",
  closure: "CLOSURE",
  cancellation: "CANCELLATION",
  "sold-out": "SOLD_OUT",
}

export function useApprovalQueueState(queueType: QueueType) {
  const [page, setPage] = useState(1)
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [selectAll, setSelectAll] = useState(false)
  const [filters, setFilters] = useState<QueueFilterState>({
    dateFrom: "",
    dateTo: "",
    agentId: "",
  })

  const queuesQuery = useQuery({
    queryKey: approvalQueries.queues(),
    queryFn: () => approvalRepository.getQueues(),
  })

  const itemsQuery = useQuery({
    queryKey: approvalQueries.queueList(queueType, { page, ...filters }),
    queryFn: () => approvalRepository.listQueueItems(queueType, { page, size: 20, ...filters }),
  })

  const backendType = QUEUE_TYPE_MAP[queueType]

  const queueMeta = useMemo(() => {
    const all = queuesQuery.data?.queues ?? []
    return {
      queues: all,
      currentQueue: all.filter((q) => q.approval_type === backendType),
    }
  }, [queuesQuery.data, backendType])

  const items = itemsQuery.data?.data ?? []
  const totalPages = itemsQuery.data?.total_pages ?? 1

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const toggleSelectAll = () => {
    if (selectAll) {
      setSelectedIds(new Set())
    } else {
      setSelectedIds(new Set(items.map((i) => i.id)))
    }
    setSelectAll(!selectAll)
  }

  const clearSelection = () => {
    setSelectedIds(new Set())
    setSelectAll(false)
  }

  const applyFilters = (updates: Partial<QueueFilterState>) => {
    setFilters((prev) => ({ ...prev, ...updates }))
    setPage(1)
  }

  return {
    queues: queueMeta.queues,
    currentQueue: queueMeta.currentQueue,
    items,
    totalPages,
    page,
    setPage,
    isLoading: itemsQuery.isLoading,
    isError: itemsQuery.isError,
    error: itemsQuery.error,
    refetch: itemsQuery.refetch,
    selectedIds,
    selectAll,
    toggleSelect,
    toggleSelectAll,
    clearSelection,
    filters,
    applyFilters,
  }
}
