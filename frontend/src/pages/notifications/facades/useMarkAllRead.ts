import { useMutation, useQueryClient } from "@tanstack/react-query"
import { notificationRepository } from "@/data/repositories/notification.repository"
import { notificationQueries } from "@/data/queries/notification.queries"
import { useToast } from "@/shared/context/toast-provider"

export function useMarkAllRead() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  return useMutation({
    mutationFn: () => notificationRepository.markAllRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationQueries.all })
      success("Đã đánh dấu tất cả là đã đọc")
    },
    onError: (err) => showError(err),
  })
}
