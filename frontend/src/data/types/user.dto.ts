export interface CreateUserRequestDTO {
  full_name: string
  username: string
  phone?: string
  email?: string
  password?: string | null
  role?: "AGENT" | "APPROVER" | "ADMIN"
}

export interface UpdateUserRequestDTO {
  full_name?: string
  phone?: string | null
  email?: string | null
  is_active?: boolean
}

export interface AssignRoleRequestDTO {
  role: "AGENT" | "APPROVER" | "ADMIN"
}

export interface UserListResponseDTO {
  data: import("./auth.dto").UserDTO[]
  page: number
  size: number
  total: number
  total_pages: number
}
