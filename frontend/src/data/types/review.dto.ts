export interface ReviewDTO {
  id: string
  listing_id: string
  author_id: string
  author_name: string
  content: string
  images: ReviewImageDTO[]
  created_at: string
  updated_at: string
}

export interface ReviewImageDTO {
  id: string
  url: string
  order: number
}

export interface ReviewListResponseDTO {
  data: ReviewDTO[]
  page: number
  size: number
  total: number
  total_pages: number
}

export interface CreateReviewRequestDTO {
  content: string
}
