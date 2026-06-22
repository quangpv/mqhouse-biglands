import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useApproveItem() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: ({ id }: { id: string }) => approvalRepository.approve(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      toast.success("Duyệt thành công")
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
