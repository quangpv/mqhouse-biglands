import axios, { type AxiosInstance } from "axios"
import { ApiError } from "./api-error"

const httpClient: AxiosInstance = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
  paramsSerializer: (params) => {
    const searchParams = new URLSearchParams()
    for (const [key, value] of Object.entries(params)) {
      if (Array.isArray(value)) {
        for (const item of value) {
          searchParams.append(key, String(item))
        }
      } else if (value !== undefined && value !== null) {
        searchParams.append(key, String(value))
      }
    }
    return searchParams.toString()
  },
})

httpClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth-token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

function errorInterceptor(error: unknown) {
  if (axios.isAxiosError(error) && error.response?.status === 401) {
    localStorage.removeItem("auth-token")
    localStorage.removeItem("auth-user")
    if (window.location.pathname !== "/dang-nhap") {
      window.location.href = "/dang-nhap"
    }
  }
  return Promise.reject(ApiError.fromAxiosError(error))
}

httpClient.interceptors.response.use(
  (response) => response,
  errorInterceptor,
)

export default httpClient
