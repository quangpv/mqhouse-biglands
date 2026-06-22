import axios, { AxiosError, type AxiosInstance } from "axios"
import type { ApiErrorDTO } from "../types/common.dto"

const httpClient: AxiosInstance = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
})

httpClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth-token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

httpClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorDTO>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("auth-token")
      localStorage.removeItem("auth-user")
      if (window.location.pathname !== "/dang-nhap") {
        window.location.href = "/dang-nhap"
      }
    }
    return Promise.reject(error)
  },
)

export default httpClient
