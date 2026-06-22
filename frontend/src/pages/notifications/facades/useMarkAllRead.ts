import { useMutation, useQueryClient } from "@tanstack/react-query"
import { notificationRepository } from "@/data/repositories/notification.repository"
import { notificationQueries } from "@/data/queries/notification.queries"
import { toast } from "sonner"

export function useMarkAllRead() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => notificationRepository.markAllRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationQueries.all })
      toast.success("Đã đánh dấu tất cả là đã đọc")
    },
  })
}
