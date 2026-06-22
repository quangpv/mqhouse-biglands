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
  fullName: string
  username: string
  phone: string | null
  email: string | null
  role: "AGENT" | "APPROVER" | "ADMIN"
  isActive: boolean
  organizationId: string | null
  organizationName: string | null
  generatedPassword: string | null
  createdBy: string | null
  createdAt: string
  updatedAt: string
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
  newPassword: string
}

export interface ResetPasswordResponseDTO {
  message: string
}
