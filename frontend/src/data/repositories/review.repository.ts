import httpClient from "../infra/http-client"
import type { ReviewListResponseDTO, ReviewDTO, CreateReviewRequestDTO } from "../types/review.dto"

export const reviewRepository = {
  list: (listingId: string) =>
    httpClient.get<ReviewListResponseDTO>(`/listings/${listingId}/reviews`).then((r) => r.data),

  create: (listingId: string, data: CreateReviewRequestDTO) =>
    httpClient.post<ReviewDTO>(`/listings/${listingId}/reviews`, data).then((r) => r.data),

  delete: (listingId: string, reviewId: string) =>
    httpClient.delete(`/listings/${listingId}/reviews/${reviewId}`).then(() => undefined),

  uploadImage: (listingId: string, reviewId: string, file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    return httpClient
      .post(`/listings/${listingId}/reviews/${reviewId}/images`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data)
  },
}
