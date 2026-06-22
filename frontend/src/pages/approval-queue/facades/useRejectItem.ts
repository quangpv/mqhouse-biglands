import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"

export function useRejectItem() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      approvalRepository.reject(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      success("Đã từ chối")
    },
    onError: (err) => showError(err),
  })
}
