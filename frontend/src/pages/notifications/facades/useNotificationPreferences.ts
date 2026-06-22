import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { notificationRepository } from "@/data/repositories/notification.repository"
import { notificationQueries } from "@/data/queries/notification.queries"
import { useToast } from "@/shared/context/toast-provider"

export interface INotificationPreferences {
  listingPostCreated: boolean
  listingPostApproved: boolean
  listingPostRejected: boolean
  depositReported: boolean
  depositConfirmed: boolean
  depositRejected: boolean
  closureReported: boolean
  closureConfirmed: boolean
  closureRejected: boolean
  cancellationReported: boolean
  cancellationConfirmed: boolean
  cancellationRejected: boolean
  soldOutReported: boolean
  soldOutConfirmed: boolean
  listingExpired: boolean
}

export function useNotificationPreferences() {
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  const query = useQuery({
    queryKey: notificationQueries.preferences(),
    queryFn: () => notificationRepository.getPreferences() as Promise<INotificationPreferences>,
  })

  const updateMutation = useMutation({
    mutationFn: (data: Record<string, boolean>) => notificationRepository.updatePreferences(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationQueries.preferences() })
      success("Đã lưu cài đặt thông báo")
    },
    onError: (err) => showError(err),
  })

  return { query, updateMutation }
}
