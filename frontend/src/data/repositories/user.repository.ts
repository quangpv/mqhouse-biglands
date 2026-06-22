import httpClient from "../infra/http-client"
import type { UserDTO } from "../types/auth.dto"
import type { UserListResponseDTO } from "../types/user.dto"

export interface UserListParams {
  page?: number
  size?: number
  role?: string
  isActive?: boolean
  search?: string
}

export const userRepository = {
  list: (params?: UserListParams) =>
    httpClient.get<UserListResponseDTO>("/users", { params }).then((r) => r.data),

  get: (id: string) =>
    httpClient.get<UserDTO>(`/users/${id}`).then((r) => r.data),

  create: (data: Record<string, unknown>) =>
    httpClient.post<UserDTO>("/users", data).then((r) => r.data),

  update: (id: string, data: Record<string, unknown>) =>
    httpClient.put<UserDTO>(`/users/${id}`, data).then((r) => r.data),

  deactivate: (id: string) =>
    httpClient.patch<UserDTO>(`/users/${id}/deactivate`).then((r) => r.data),

  reactivate: (id: string) =>
    httpClient.patch<UserDTO>(`/users/${id}/reactivate`).then((r) => r.data),

  assignRole: (id: string, role: string) =>
    httpClient.patch<UserDTO>(`/users/${id}/role`, { role }).then((r) => r.data),
}
