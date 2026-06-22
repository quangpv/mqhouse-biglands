import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useRemoveHot() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ listingId }: { listingId: string }) =>
      listingRepository.unpromoteFromHot(listingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã xoá khỏi danh sách nổi bật")
    },
    onError: (err) => showError(err),
  })
}
