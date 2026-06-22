export interface PaginationDTO {
  page: number
  size: number
  total: number
  total_pages: number
}

export interface ApiErrorDTO {
  code: string
  message: string
  details?: Array<{
    field: string
    message: string
    code: string
  }>
}

export interface ValidationErrorDTO {
  code: "VALIDATION_ERROR"
  message: string
  details: Array<{
    field: string
    message: string
    code: string
  }>
}
