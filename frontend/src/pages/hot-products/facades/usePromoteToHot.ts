import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function usePromoteToHot() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ listingId, hotOrder }: { listingId: string; hotOrder: number }) =>
      listingRepository.promoteToHot(listingId, hotOrder),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã thêm vào tin nổi bật")
    },
    onError: (err) => showError(err),
  })
}
