import { useMutation, useQueryClient } from "@tanstack/react-query"
import { reviewRepository } from "@/data/repositories/review.repository"
import { reviewQueries } from "@/data/queries/review.queries"
import { toast } from "sonner"

export function useCreateReview(listingId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { content: string; images: File[] }) => {
      const review = await reviewRepository.create(listingId, { content: data.content })
      for (const file of data.images) {
        await reviewRepository.uploadImage(listingId, review.id, file)
      }
      return review
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewQueries.list(listingId) })
      toast.success("Đã gửi đánh giá")
    },
    onError: () => {
      toast.error("Không thể gửi đánh giá")
    },
  })
}
