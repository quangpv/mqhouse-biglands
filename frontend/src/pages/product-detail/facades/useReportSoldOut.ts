import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useReportSoldOut(listingId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (notes: string) =>
      dealEventRepository.reportSoldOut(listingId, { notes: notes || undefined }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      toast.success("Báo hết hàng thành công, chờ duyệt")
    },
    onError: () => {
      toast.error("Không thể báo hết hàng")
    },
  })
}
