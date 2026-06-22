import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { authRepository } from "@/data/repositories/auth.repository"
import type { IResetPasswordForm } from "../types"
import type { ResetPasswordResponseDTO } from "@/data/types/auth.dto"

interface ResetPasswordInput extends IResetPasswordForm {
  token: string
}

export function useResetPassword() {
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (data: ResetPasswordInput) =>
      authRepository.resetPassword({ token: data.token, newPassword: data.newPassword }),
    onSuccess: (_res: ResetPasswordResponseDTO) => {
      toast.success("Đặt lại mật khẩu thành công")
      navigate("/dang-nhap", { replace: true })
    },
  })
}
