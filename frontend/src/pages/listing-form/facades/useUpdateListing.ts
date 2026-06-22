import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { formToCreatePayload, type IListingForm } from "../types"

export function useUpdateListing(listingId: string) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: async (data: IListingForm) => {
      const payload = formToCreatePayload(data)
      return listingRepository.update(listingId, payload as unknown as Record<string, unknown>)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.all })
      queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
      navigate(`/tin/${listingId}`)
    },
    onError: () => {
      toast.error("Không thể cập nhật tin đăng. Vui lòng thử lại.")
    },
  })

  return { mutation }
}
