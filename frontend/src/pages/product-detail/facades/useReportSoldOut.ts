import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useReportSoldOut(listingId: string, role?: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (notes: string) =>
      dealEventRepository.reportSoldOut(listingId, { notes: notes || undefined }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      success(role === "ADMIN" ? "Báo hết hàng thành công" : "Báo hết hàng thành công, chờ duyệt")
    },
    onError: (err) => showError(err),
  })
}
