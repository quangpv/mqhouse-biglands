import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import type { ApiError } from "@/data/infra/api-error"

export function useAssignRole() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, role }: { id: string; role: "AGENT" | "APPROVER" | "ADMIN" }) =>
      userRepository.assignRole(id, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      toast.success("Đã thay đổi vai trò")
    },
    onError: (error: ApiError) => {
      if (error.code === "LAST_ADMIN") {
        toast.error("Không thể thay đổi ADMIN cuối cùng")
      } else {
        toast.error(error.message || "Có lỗi xảy ra")
      }
    },
  })
}
