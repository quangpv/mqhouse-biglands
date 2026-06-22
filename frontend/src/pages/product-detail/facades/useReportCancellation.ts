import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { IReportCancellationForm } from "../types"

export function useReportCancellation(listingId: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: IReportCancellationForm) =>
      dealEventRepository.reportCancellation(listingId, { notes: data.notes }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      success("Báo huỷ cọc thành công, chờ duyệt")
    },
    onError: (err) => showError(err),
  })
}
