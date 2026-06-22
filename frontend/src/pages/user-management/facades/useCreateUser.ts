import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { ApiError } from "@/data/infra/api-error"
import type { IUserFormData } from "../types"

export function useCreateUser() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (data: IUserFormData) =>
      userRepository.create({
        fullName: data.fullName,
        username: data.username,
        phone: data.phone || undefined,
        email: data.email || undefined,
        password: data.password || null,
        role: data.role,
      }),
    onSuccess: (user) => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      if (user.generatedPassword) {
        toast.success(`Tạo người dùng thành công. Mật khẩu: ${user.generatedPassword}`)
      } else {
        toast.success("Tạo người dùng thành công")
      }
      navigate("/nguoi-dung")
    },
    onError: (error: ApiError) => {
      if (error.code === "USERNAME_TAKEN") {
        toast.error("Tên đăng nhập đã tồn tại")
      } else {
        toast.error(error.message || "Có lỗi xảy ra")
      }
    },
  })
}
