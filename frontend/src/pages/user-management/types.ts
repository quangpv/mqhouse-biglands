export interface IUserFormData {
  fullName: string
  username: string
  phone: string
  email: string
  role: "AGENT" | "APPROVER" | "ADMIN"
  password: string
  isActive: boolean
}

export interface IUserTableRow {
  id: string
  fullName: string
  username: string
  phone: string | null
  role: string
  roleLabel: string
  isActive: boolean
  organizationName: string | null
  createdAt: string
}
