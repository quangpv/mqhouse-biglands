export interface LoginRequestDTO {
  username: string
  password: string
}

export interface LoginResponseDTO {
  token: string
  user: UserDTO
}

export interface UserDTO {
  id: string
  full_name: string
  username: string
  phone: string | null
  email: string | null
  role: "AGENT" | "APPROVER" | "ADMIN"
  is_active: boolean
  organization_id: string | null
  organization_name: string | null
  generated_password: string | null
  created_by: string | null
  created_at: string
  updated_at: string
}

export interface ForgotPasswordRequestDTO {
  username: string
}

export interface ForgotPasswordResponseDTO {
  token: string
  message: string
}

export interface ResetPasswordRequestDTO {
  token: string
  new_password: string
}

export interface ResetPasswordResponseDTO {
  message: string
}
