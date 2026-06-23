import { useState } from "react"
import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { useAuthStore } from "@/shared/context/auth-store"
import type { IReportCancellationForm } from "../types"

type DialogType = "deposit" | "closure" | "cancellation" | "sold-out" | "approve" | "reject" | null

export function useProductDetailState() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuthStore()
  const [activeDialog, setActiveDialog] = useState<DialogType>(null)
  const [ownerPhoneVisible, setOwnerPhoneVisible] = useState(false)

  const query = useQuery({
    queryKey: listingQueries.detail(id!),
    queryFn: () => listingRepository.get(id!),
    enabled: !!id,
  })

  const cancellationForm = useForm<IReportCancellationForm>({
    resolver: zodResolver(z.object({ notes: z.string().min(1, "Vui lòng nhập lý do") })),
    defaultValues: { notes: "" },
  })

  const listing = query.data ?? null
  const isOwner = user ? listing?.created_by_id === user.id : false
  const isApprover = user?.role === "APPROVER" || user?.role === "ADMIN"

  const openDialog = (type: DialogType) => {
    setActiveDialog(type)
    if (type === "cancellation") cancellationForm.reset()
  }
  const closeDialog = () => setActiveDialog(null)

  return {
    id,
    listing,
    isOwner,
    isApprover,
    query,
    activeDialog,
    openDialog,
    closeDialog,
    cancellationForm,
    ownerPhoneVisible,
    setOwnerPhoneVisible,
  }
}
