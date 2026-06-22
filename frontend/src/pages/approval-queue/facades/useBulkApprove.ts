import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useBulkApprove() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ ids }: { ids: string[] }) => approvalRepository.bulkApprove(ids),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      const failedCount = data.failed.length
      if (failedCount === 0) {
        toast.success(`Đã duyệt ${data.succeeded.length} yêu cầu`)
      } else {
        toast.warning(`Duyệt thành công ${data.succeeded.length}, ${failedCount} yêu cầu thất bại`)
      }
    },
    onError: (error: ApiError) => {
      toast.error(error.message || "Có lỗi xảy ra, vui lòng thử lại")
    },
  })
}
