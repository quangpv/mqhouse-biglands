import { useMutation, useQueryClient } from "@tanstack/react-query"
import { reviewRepository } from "@/data/repositories/review.repository"
import { reviewQueries } from "@/data/queries/review.queries"
import { useToast } from "@/shared/context/toast-provider"

export function useDeleteReview(listingId: string) {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (reviewId: string) => reviewRepository.delete(listingId, reviewId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewQueries.list(listingId) })
      success("Đã xoá đánh giá")
    },
    onError: (err) => showError(err),
  })
}
