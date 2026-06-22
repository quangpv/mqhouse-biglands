import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useDeactivateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) =>
      isActive ? userRepository.deactivate(id) : userRepository.reactivate(id),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      queryClient.invalidateQueries({ queryKey: userQueries.all })
      toast.success(variables.isActive ? "Đã vô hiệu hoá người dùng" : "Đã kích hoạt lại người dùng")
    },
    onError: (error: ApiError) => {
      if (error.code === "LAST_ADMIN") {
        toast.error("Không thể vô hiệu hoá ADMIN cuối cùng")
      } else {
        toast.error(error.message || "Có lỗi xảy ra")
      }
    },
  })
}
