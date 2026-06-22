import { useSearchParams } from "react-router-dom"
import { useResetPasswordState } from "./facades/useResetPasswordState"
import { useResetPassword } from "./facades/useResetPassword"
import { ResetPasswordForm } from "./components/ResetPasswordForm"
import type { AxiosError } from "axios"
import type { ApiErrorDTO } from "@/data/types/common.dto"

function getErrorMessage(error: unknown): string | undefined {
  if (!error) return undefined
  const axiosError = error as AxiosError<ApiErrorDTO>
  const status = axiosError.response?.status
  if (status === 401 || status === 400) {
    return "Liên kết không hợp lệ hoặc đã hết hạn"
  }
  return "Có lỗi xảy ra, vui lòng thử lại"
}

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get("token")
  const { form } = useResetPasswordState()
  const { mutate, isPending, error } = useResetPassword()
  const message = getErrorMessage(error)

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
        <div className="w-full max-w-sm text-center space-y-4">
          <div className="text-3xl font-bold tracking-tight">Biglands</div>
          <p className="text-muted-foreground">Liên kết không hợp lệ hoặc đã hết hạn</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center space-y-2">
          <div className="text-3xl font-bold tracking-tight">Biglands</div>
          <p className="text-lg font-medium text-muted-foreground">Đặt lại mật khẩu</p>
        </div>

        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <ResetPasswordForm
            form={form}
            onSubmit={(data) => mutate({ ...data, token })}
            isPending={isPending}
            error={message}
          />
        </div>
      </div>
    </div>
  )
}
