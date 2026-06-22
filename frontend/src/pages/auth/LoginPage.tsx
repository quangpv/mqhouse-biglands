import { useLoginState } from "./facades/useLoginState"
import { useLogin } from "./facades/useLogin"
import { LoginForm } from "./components/LoginForm"
import { getLoginErrorMessage } from "./mappers/login-error-mapper"

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
