import { useMutation, useQueryClient } from "@tanstack/react-query"
import { reviewRepository } from "@/data/repositories/review.repository"
import { reviewQueries } from "@/data/queries/review.queries"
import { toast } from "sonner"
import { useAuthStore } from "@/shared/context/auth-store"

export function useDeleteReview(listingId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (reviewId: string) => reviewRepository.delete(listingId, reviewId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewQueries.list(listingId) })
      toast.success("Đã xoá đánh giá")
    },
    onError: () => {
      toast.error("Không thể xoá đánh giá")
    },
  })
}
