import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { IUserFormData } from "../types"

export function useCreateUser() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: IUserFormData) =>
      userRepository.create({
        full_name: data.fullName,
        username: data.username,
        phone: data.phone || undefined,
        email: data.email || undefined,
        password: data.password || null,
        role: data.role,
      }),
    onSuccess: (user) => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      if (user.generatedPassword) {
        success(`Tạo người dùng thành công. Mật khẩu: ${user.generatedPassword}`)
      } else {
        success("Tạo người dùng thành công")
      }
      navigate("/nguoi-dung")
    },
    onError: (err) => showError(err),
  })
}
