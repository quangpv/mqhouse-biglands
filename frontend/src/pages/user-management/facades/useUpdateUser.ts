import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { IUserFormData } from "../types"

export function useUpdateUser(userId: string) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: (data: IUserFormData) =>
      userRepository.update(userId, {
        full_name: data.fullName,
        phone: data.phone || null,
        email: data.email || null,
        is_active: data.isActive,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      queryClient.invalidateQueries({ queryKey: userQueries.detail(userId) })
      success("Cập nhật người dùng thành công")
      navigate("/nguoi-dung")
    },
    onError: (err) => showError(err),
  })
}
