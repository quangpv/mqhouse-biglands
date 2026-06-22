import { useMutation, useQueryClient } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { toast } from "sonner"

export function useWithdrawListing() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => listingRepository.withdraw(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Đã rút tin về nháp")
    },
    onError: () => {
      toast.error("Không thể rút tin này")
    },
  })
}
