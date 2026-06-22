import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useReportClosure(listingId: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (notes: string) =>
      dealEventRepository.reportClosure(listingId, { notes: notes || undefined }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      success("Báo chốt hàng thành công, chờ duyệt")
    },
    onError: (err) => showError(err),
  })
}
