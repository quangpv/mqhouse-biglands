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
    fullName: user.fullName,
    username: user.username,
    phone: user.phone,
    role: user.role,
    roleLabel: user.organizationName ?? roleLabels[user.role] ?? user.role,
    isActive: user.isActive,
    organizationName: user.organizationName,
    createdAt: user.createdAt,
  }
}
