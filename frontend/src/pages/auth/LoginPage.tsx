import { useLoginState } from "./facades/useLoginState"
import { useLogin } from "./facades/useLogin"
import { LoginForm } from "./components/LoginForm"
import type { AxiosError } from "axios"
import type { ApiErrorDTO } from "@/data/types/common.dto"

function getLoginErrorMessage(error: unknown): string | undefined {
  if (!error) return undefined
  const axiosError = error as AxiosError<ApiErrorDTO>
  const status = axiosError.response?.status
  const code = axiosError.response?.data?.code

  if (status === 403 && code === "ACCOUNT_DEACTIVATED") {
    return "Tài khoản đã bị vô hiệu hoá"
  }
  if (status === 401) {
    return "Sai tên đăng nhập hoặc mật khẩu"
  }
  return "Có lỗi xảy ra, vui lòng thử lại"
}

export default function LoginPage() {
  const { form } = useLoginState()
  const { mutate, isPending, error } = useLogin()
  const message = getLoginErrorMessage(error)

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center space-y-2">
          <div className="text-3xl font-bold tracking-tight">Biglands</div>
          <p className="text-lg font-medium text-muted-foreground">Đăng nhập quản lý</p>
        </div>

        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <LoginForm form={form} onSubmit={(data) => mutate(data)} isPending={isPending} error={message} />
        </div>
      </div>
    </div>
  )
}
