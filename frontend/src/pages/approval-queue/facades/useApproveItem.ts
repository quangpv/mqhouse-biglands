import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"

export function useApproveItem() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ id }: { id: string }) => approvalRepository.approve(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: approvalQueries.queues() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      success("Duyệt thành công")
    },
    onError: (err) => showError(err),
  })
}
