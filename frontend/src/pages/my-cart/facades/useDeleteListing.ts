import { useMutation, useQueryClient } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { toast } from "sonner"

export function useDeleteListing() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => listingRepository.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success("Đã xoá tin nháp")
    },
    onError: () => {
      toast.error("Không thể xoá tin này")
    },
  })
}
