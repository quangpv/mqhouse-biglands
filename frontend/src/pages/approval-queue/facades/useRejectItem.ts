import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useRejectItem() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      approvalRepository.reject(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      toast.success("Đã từ chối")
    },
    onError: (error: ApiError) => {
      if (error.code === "ALREADY_PROCESSED") {
        toast.error("Yêu cầu đã được xử lý")
      } else {
        toast.error(error.message || "Có lỗi xảy ra, vui lòng thử lại")
      }
    },
  })
}
