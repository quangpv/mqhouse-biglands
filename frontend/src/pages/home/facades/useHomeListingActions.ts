import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { approvalRepository } from "@/data/repositories/approval.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { approvalQueries } from "@/data/queries/approval.queries"
import { useToast } from "@/shared/context/toast-provider"
import type { IListing } from "@/shared/types/listing.type"

export type HomeActionType =
  | "approve"
  | "reject"
  | "blocked-edit"
  | "blocked-delete"

interface ActionDialogState {
  listing: IListing
  type: HomeActionType
}

export function useHomeListingActions() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { success, showError } = useToast()

  const [actionDialog, setActionDialog] = useState<ActionDialogState | null>(null)

  const closeDialog = () => setActionDialog(null)

  const approveMutation = useMutation({
    mutationFn: (id: string) => approvalRepository.approve(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      success("Duyệt thành công")
      closeDialog()
    },
    onError: (err) => showError(err),
  })

  const rejectMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      approvalRepository.reject(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      queryClient.invalidateQueries({ queryKey: approvalQueries.all })
      success("Đã từ chối")
      closeDialog()
    },
    onError: (err) => showError(err),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => listingRepository.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      success("Đã xoá tin")
      closeDialog()
    },
    onError: (err) => showError(err),
  })

  const promoteToHotMutation = useMutation({
    mutationFn: (id: string) => listingRepository.promoteToHot(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.hotStrip() })
      success("Đã thêm vào tin nổi bật")
    },
    onError: (err) => showError(err),
  })

  const unpromoteFromHotMutation = useMutation({
    mutationFn: (id: string) => listingRepository.unpromoteFromHot(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      queryClient.invalidateQueries({ queryKey: listingQueries.hot() })
      queryClient.invalidateQueries({ queryKey: listingQueries.hotStrip() })
      success("Đã bỏ ghim hot")
    },
    onError: (err) => showError(err),
  })

  const handleApprove = (listing: IListing) => {
    setActionDialog({ listing, type: "approve" })
  }

  const handleReject = (listing: IListing) => {
    setActionDialog({ listing, type: "reject" })
  }

  const handleEdit = (listing: IListing) => {
    navigate(`/tin/${listing.id}/chinh-sua`)
  }

  const handleDelete = (listing: IListing) => {
    deleteMutation.mutate(listing.id)
  }

  const handleBlockedAction = (listing: IListing, action: "edit" | "delete") => {
    setActionDialog({
      listing,
      type: action === "edit" ? "blocked-edit" : "blocked-delete",
    })
  }

  const handlePromoteToHot = (listing: IListing) => {
    promoteToHotMutation.mutate(listing.id)
  }

  const handleUnpromoteFromHot = (listing: IListing) => {
    unpromoteFromHotMutation.mutate(listing.id)
  }

  const confirmApprove = () => {
    if (actionDialog) approveMutation.mutate(actionDialog.listing.id)
  }

  const confirmReject = (reason: string) => {
    if (actionDialog)
      rejectMutation.mutate({ id: actionDialog.listing.id, reason })
  }

  return {
    actionDialog,
    closeDialog,
    handleApprove,
    handleReject,
    handleEdit,
    handleDelete,
    handleBlockedAction,
    handlePromoteToHot,
    handleUnpromoteFromHot,
    confirmApprove,
    confirmReject,
    isApproving: approveMutation.isPending,
    isRejecting: rejectMutation.isPending,
  }
}
