import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { ApiError } from "@/data/infra/api-error"
import type { IUserFormData } from "../types"

export function useUpdateUser(userId: string) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (data: IUserFormData) =>
      userRepository.update(userId, {
        fullName: data.fullName,
        phone: data.phone || null,
        email: data.email || null,
        isActive: data.isActive,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      queryClient.invalidateQueries({ queryKey: userQueries.detail(userId) })
      toast.success("Cập nhật người dùng thành công")
      navigate("/nguoi-dung")
    },
    onError: (error: ApiError) => {
      toast.error(error.message || "Có lỗi xảy ra")
    },
  })
}
