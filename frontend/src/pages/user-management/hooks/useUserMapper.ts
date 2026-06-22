import type { UserDTO } from "@/data/types/auth.dto"
import type { IUserTableRow } from "../types"

const roleLabels: Record<string, string> = {
  AGENT: "Môi giới",
  APPROVER: "Người duyệt",
  ADMIN: "Quản trị viên",
}

export function toUserTableRow(user: UserDTO): IUserTableRow {
  return {
    id: user.id,
    fullName: user.full_name,
    username: user.username,
    phone: user.phone,
    role: user.role,
    roleLabel: user.organization_name ?? roleLabels[user.role] ?? user.role,
    isActive: user.is_active,
    organizationName: user.organization_name,
    createdAt: user.created_at,
  }
}
