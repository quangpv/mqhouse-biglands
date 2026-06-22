import { ApiError } from "@/data/infra/api-error"

export function getLoginErrorMessage(error: unknown): string | undefined {
  if (!error) return undefined
  if (error instanceof ApiError) {
    if (error.code === "ACCOUNT_DEACTIVATED") {
      return "Tài khoản đã bị vô hiệu hoá"
    }
    if (error.status === 401) {
      return "Sai tên đăng nhập hoặc mật khẩu"
    }
    return error.message
  }
  return "Có lỗi xảy ra, vui lòng thử lại"
}
