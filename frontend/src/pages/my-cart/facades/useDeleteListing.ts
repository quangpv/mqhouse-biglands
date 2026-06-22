import { useMutation, useQueryClient } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { useToast } from "@/shared/context/toast-provider"

export function useDeleteListing() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (id: string) => listingRepository.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã xoá tin nháp")
    },
    onError: (err) => showError(err),
  })
}
