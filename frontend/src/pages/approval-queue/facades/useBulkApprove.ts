import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"

export function useBulkApprove() {
  const queryClient = useQueryClient()
  const { success, warning, showError } = useToast()

  return useMutation({
    mutationFn: ({ ids }: { ids: string[] }) => approvalRepository.bulkApprove(ids),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      const failedCount = data.failed.length
      if (failedCount === 0) {
        success(`Đã duyệt ${data.succeeded.length} yêu cầu`)
      } else {
        warning(`Duyệt thành công ${data.succeeded.length}, ${failedCount} yêu cầu thất bại`)
      }
    },
    onError: (err) => showError(err),
  })
}
