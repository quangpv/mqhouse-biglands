import { useMutation, useQueryClient } from "@tanstack/react-query"
import { notificationRepository } from "@/data/repositories/notification.repository"
import { notificationQueries } from "@/data/queries/notification.queries"

export function useMarkRead() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => notificationRepository.markRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationQueries.lists() })
      queryClient.invalidateQueries({ queryKey: notificationQueries.unreadCount() })
    },
  })
}
