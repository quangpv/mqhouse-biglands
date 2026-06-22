import httpClient from "../infra/http-client"
import type { LoginRequestDTO, LoginResponseDTO, ForgotPasswordRequestDTO, ResetPasswordRequestDTO, UserDTO } from "../types/auth.dto"

export const authRepository = {
  login: (data: LoginRequestDTO) =>
    httpClient.post<LoginResponseDTO>("/auth/login", data).then((r) => r.data),

  me: () =>
    httpClient.get<UserDTO>("/auth/me").then((r) => r.data),

  forgotPassword: (data: ForgotPasswordRequestDTO) =>
    httpClient.post("/auth/forgot-password", data).then((r) => r.data),

  resetPassword: (data: ResetPasswordRequestDTO) =>
    httpClient.post("/auth/reset-password", data).then((r) => r.data),
}
