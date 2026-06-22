import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useRemoveHot() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ listingId }: { listingId: string }) =>
      listingRepository.unpromoteFromHot(listingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Đã xoá khỏi danh sách nổi bật")
    },
    onError: (error: ApiError) => {
      toast.error(error.message || "Có lỗi xảy ra")
    },
  })
}
