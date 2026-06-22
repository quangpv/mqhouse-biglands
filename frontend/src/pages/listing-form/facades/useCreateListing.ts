import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { formToCreatePayload, type IListingForm } from "../types"

export function useCreateListing() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [images, setImages] = useState<File[]>([])
  const [listingId, setListingId] = useState<string | null>(null)

  const mutation = useMutation({
    mutationFn: async (data: IListingForm) => {
      const payload = formToCreatePayload(data)
      const result = await listingRepository.create(payload as unknown as Record<string, unknown>)
      const id = result.id as string
      setListingId(id)

      if (images.length > 0) {
        for (const file of images) {
          const formData = new FormData()
          formData.append("file", file)
          await listingRepository.uploadImage(id, formData)
        }
      }
      return result
    },
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: listingQueries.all })
      const id = result.id as string
      navigate(`/tin/${id}`)
    },
    onError: () => {
      toast.error("Không thể tạo tin đăng. Vui lòng thử lại.")
    },
  })

  return { mutation, images, setImages, listingId }
}
