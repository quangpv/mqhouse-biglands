import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { dealEventRepository } from "@/data/repositories/deal-event.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { IReportDepositForm } from "../types"

export function useReportDeposit(listingId: string, role?: string) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: IReportDepositForm) =>
      dealEventRepository.reportDeposit(listingId, {
        customer_name: data.customerName,
        customer_phone: data.customerPhone || undefined,
        deposit_amount: data.depositAmount,
        notes: data.notes || undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success(role === "ADMIN" ? "Báo cọc thành công" : "Báo cọc thành công, chờ duyệt")
      navigate(".", { replace: true })
    },
    onError: (err) => showError(err),
  })
}
