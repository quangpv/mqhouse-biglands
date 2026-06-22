import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useToast } from "@/shared/context/toast-provider"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { formToCreatePayload, type IListingForm } from "../types"

export function useCreateListing() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [images, setImages] = useState<File[]>([])
  const [listingId, setListingId] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const { showError } = useToast()

  const mutation = useMutation({
    mutationFn: async ({ data, action }: { data: IListingForm; action: "draft" | "submit" }) => {
      setIsSaving(action === "draft")
      const payload = formToCreatePayload({ ...data, action })
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
    onSettled: () => setIsSaving(false),
    onError: (err) => showError(err),
  })

  return { mutation, images, setImages, listingId, isSaving }
}
