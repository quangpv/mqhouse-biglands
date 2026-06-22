import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { authRepository } from "@/data/repositories/auth.repository"
import type { IForgotPasswordForm } from "../types"
import type { ForgotPasswordResponseDTO } from "@/data/types/auth.dto"

export function useForgotPassword() {
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (data: IForgotPasswordForm) => authRepository.forgotPassword(data),
    onSuccess: (res: ForgotPasswordResponseDTO) => {
      toast.success("Vui lòng kiểm tra email để đặt lại mật khẩu")
      navigate(`/dat-lai-mat-khau?token=${res.token}`, { replace: true })
    },
  })
}
