import type { AxiosError } from "axios"

export class ApiError extends Error {
  readonly code: string
  readonly status: number

  constructor(code: string, message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.code = code
    this.status = status
  }

  static fromAxiosError(error: AxiosError<unknown>): ApiError {
    const data = error.response?.data as Record<string, unknown> | undefined
    const code = (data?.code as string) || "UNKNOWN_ERROR"
    const detail = data?.detail
    let message: string
    if (typeof detail === "string") {
      message = detail
    } else if (Array.isArray(detail)) {
      message = detail.map((d: Record<string, unknown>) => String(d.msg ?? "")).filter(Boolean).join("; ")
    } else {
      message = (data?.message as string) || error.message || "Có lỗi xảy ra"
    }
    return new ApiError(code, message, error.response?.status ?? 500)
  }
}
