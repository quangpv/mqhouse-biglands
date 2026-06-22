import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useSubmitListing(listingId: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: () => listingRepository.submit(listingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã gửi yêu cầu duyệt")
    },
    onError: (err) => showError(err),
  })
}
