export interface OrganizationDTO {
  id: string
  name: string
  displayName: string
  createdAt: string
  updatedAt: string
}

export interface CreateOrganizationRequestDTO {
  name: string
  displayName: string
}

export interface UpdateOrganizationRequestDTO {
  displayName: string
}

export interface OrganizationListResponseDTO {
  data: OrganizationDTO[]
  pagination: import("./common.dto").PaginationDTO
}
