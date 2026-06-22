import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { ApiError } from "@/data/infra/api-error"

export function usePromoteToHot() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ listingId, hotOrder }: { listingId: string; hotOrder: number }) =>
      listingRepository.promoteToHot(listingId, hotOrder),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Đã thêm vào tin nổi bật")
    },
    onError: (error: ApiError) => {
      if (error.code === "MAX_HOT_ITEMS") {
        toast.error("Đã đạt số lượng HOT tối đa (14)")
      } else if (error.code === "INVALID_STATUS_TRANSITION") {
        toast.error("Chỉ có thể thêm tin đang bán")
      } else {
        toast.error(error.message || "Có lỗi xảy ra")
      }
    },
  })
}
