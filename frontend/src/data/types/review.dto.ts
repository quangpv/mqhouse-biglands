export interface ReviewDTO {
  id: string
  listingId: string
  authorId: string
  authorName: string
  content: string
  images: ReviewImageDTO[]
  createdAt: string
  updatedAt: string
}

export interface ReviewImageDTO {
  id: string
  url: string
  order: number
}

export interface ReviewListResponseDTO {
  data: ReviewDTO[]
  pagination: {
    page: number
    size: number
    totalItems: number
    totalPages: number
  }
}

export interface CreateReviewRequestDTO {
  content: string
}
