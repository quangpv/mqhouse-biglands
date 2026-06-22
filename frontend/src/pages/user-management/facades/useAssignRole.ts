import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"

export function useAssignRole() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ id, role }: { id: string; role: "AGENT" | "APPROVER" | "ADMIN" }) =>
      userRepository.assignRole(id, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      success("Đã thay đổi vai trò")
    },
    onError: (err) => showError(err),
  })
}
