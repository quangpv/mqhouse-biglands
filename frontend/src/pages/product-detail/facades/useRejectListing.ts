import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { approvalQueries } from "@/data/queries/approval.queries"
import { listingQueries } from "@/data/queries/listing.queries"

export function useRejectListing(listingId: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (reason: string) => approvalRepository.reject(listingId, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      success("Đã từ chối")
    },
    onError: (err) => showError(err),
  })
}
