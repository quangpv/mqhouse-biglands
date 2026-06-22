import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"

export function useReportClosure(listingId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (notes: string) =>
      dealEventRepository.reportClosure(listingId, { notes: notes || undefined }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      toast.success("Báo chốt hàng thành công, chờ duyệt")
    },
    onError: () => {
      toast.error("Không thể báo chốt hàng")
    },
  })
}
