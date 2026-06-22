import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { IReportDepositForm } from "../types"

export function useReportDeposit(listingId: string) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (data: IReportDepositForm) =>
      dealEventRepository.reportDeposit(listingId, {
        customerName: data.customerName,
        customerPhone: data.customerPhone || undefined,
        depositAmount: data.depositAmount,
        notes: data.notes || undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Báo cọc thành công, chờ duyệt")
      navigate(".", { replace: true })
    },
    onError: () => {
      toast.error("Bất động sản này đã được báo cọc trước đó")
    },
  })
}
