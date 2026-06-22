import { useForgotPasswordState } from "./facades/useForgotPasswordState"
import { useForgotPassword } from "./facades/useForgotPassword"
import { ForgotPasswordForm } from "./components/ForgotPasswordForm"
import type { AxiosError } from "axios"
import type { ApiErrorDTO } from "@/data/types/common.dto"

function getErrorMessage(error: unknown): string | undefined {
  if (!error) return undefined
  const axiosError = error as AxiosError<ApiErrorDTO>
  const status = axiosError.response?.status
  if (status === 404) {
    return "Tên đăng nhập không tồn tại"
  }
  return "Có lỗi xảy ra, vui lòng thử lại"
}

export default function ForgotPasswordPage() {
  const { form } = useForgotPasswordState()
  const { mutate, isPending, error } = useForgotPassword()
  const message = getErrorMessage(error)

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center space-y-2">
          <div className="text-3xl font-bold tracking-tight">Biglands</div>
          <p className="text-lg font-medium text-muted-foreground">Quên mật khẩu</p>
        </div>

        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <ForgotPasswordForm form={form} onSubmit={(data) => mutate(data)} isPending={isPending} error={message} />
        </div>
      </div>
    </div>
  )
}
