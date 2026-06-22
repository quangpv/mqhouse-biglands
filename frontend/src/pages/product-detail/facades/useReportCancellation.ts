import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { IReportCancellationForm } from "../types"

export function useReportCancellation(listingId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: IReportCancellationForm) =>
      dealEventRepository.reportCancellation(listingId, { notes: data.notes }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      toast.success("Báo huỷ cọc thành công, chờ duyệt")
    },
    onError: () => {
      toast.error("Không thể báo huỷ cọc")
    },
  })
}
