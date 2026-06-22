import { useQuery } from "@tanstack/react-query"
import { reviewRepository } from "@/data/repositories/review.repository"
import { reviewQueries } from "@/data/queries/review.queries"

export function useReviewState(listingId: string) {
  const query = useQuery({
    queryKey: reviewQueries.list(listingId),
    queryFn: () => reviewRepository.list(listingId),
    enabled: !!listingId,
  })

  const reviews = query.data?.data ?? []

  return { query, reviews }
}
