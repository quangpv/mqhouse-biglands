import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useReorderHot() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (order: Array<{ listingId: string; hotOrder: number }>) =>
      listingRepository.reorderHotListings(order),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã cập nhật thứ tự")
    },
    onError: (err) => showError(err),
  })
}
