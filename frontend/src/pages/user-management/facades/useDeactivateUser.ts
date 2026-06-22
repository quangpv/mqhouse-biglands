import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useToast } from "@/shared/context/toast-provider"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"

export function useDeactivateUser() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) =>
      isActive ? userRepository.deactivate(id) : userRepository.reactivate(id),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: userQueries.lists() })
      queryClient.invalidateQueries({ queryKey: userQueries.all })
      success(variables.isActive ? "Đã vô hiệu hoá người dùng" : "Đã kích hoạt lại người dùng")
    },
    onError: (err) => showError(err),
  })
}
