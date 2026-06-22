export interface OrganizationDTO {
  id: string
  name: string
  display_name: string
  created_at: string
  updated_at: string
}

export interface CreateOrganizationRequestDTO {
  name: string
  display_name: string
}

export interface UpdateOrganizationRequestDTO {
  display_name: string
}

export interface OrganizationListResponseDTO {
  data: OrganizationDTO[]
  page: number
  size: number
  total: number
  total_pages: number
}
