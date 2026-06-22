export interface CreateUserRequestDTO {
  fullName: string
  username: string
  phone?: string
  email?: string
  password?: string | null
  role?: "AGENT" | "APPROVER" | "ADMIN"
}

export interface UpdateUserRequestDTO {
  fullName?: string
  phone?: string | null
  email?: string | null
  isActive?: boolean
}

export interface AssignRoleRequestDTO {
  role: "AGENT" | "APPROVER" | "ADMIN"
}

export interface UserListResponseDTO {
  data: import("./auth.dto").UserDTO[]
  pagination: import("./common.dto").PaginationDTO
}
