import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { authRepository } from "@/data/repositories/auth.repository"
import type { IForgotPasswordForm } from "../types"
import type { ForgotPasswordResponseDTO } from "@/data/types/auth.dto"

export function useForgotPassword() {
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: IForgotPasswordForm) => authRepository.forgotPassword(data),
    onSuccess: (res: ForgotPasswordResponseDTO) => {
      success("Vui lòng kiểm tra email để đặt lại mật khẩu")
      navigate(`/dat-lai-mat-khau?token=${res.token}`, { replace: true })
    },
    onError: (err) => showError(err),
  })
}
