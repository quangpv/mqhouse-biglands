import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useReorderHot() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (order: Array<{ listingId: string; hotOrder: number }>) =>
      listingRepository.reorderHotListings(order),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Đã cập nhật thứ tự")
    },
    onError: (error: ApiError) => {
      toast.error(error.message || "Có lỗi xảy ra")
    },
  })
}
