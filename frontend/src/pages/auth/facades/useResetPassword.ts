import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { authRepository } from "@/data/repositories/auth.repository"
import type { IResetPasswordForm } from "../types"
import type { ResetPasswordResponseDTO } from "@/data/types/auth.dto"

interface ResetPasswordInput extends IResetPasswordForm {
  token: string
}

export function useResetPassword() {
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: ResetPasswordInput) =>
      authRepository.resetPassword({ token: data.token, newPassword: data.newPassword }),
    onSuccess: (_res: ResetPasswordResponseDTO) => {
      success("Đặt lại mật khẩu thành công")
      navigate("/dang-nhap", { replace: true })
    },
    onError: (err) => showError(err),
  })
}
