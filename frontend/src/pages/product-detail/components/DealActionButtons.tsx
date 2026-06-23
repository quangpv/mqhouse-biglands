import { Button } from "@/shared/components/ui/button"
import { Heart, Share2, Pencil, Trash2 } from "lucide-react"
import { Link } from "react-router-dom"
import type { ListingDetailResponseDTO } from "@/data/types/listing.dto"

const BLOCKED_STATUSES = ["DA_COC", "DA_CHOT", "HET_HANG", "HUY_COC", "QUA_HAN"]

interface DealActionButtonsProps {
  listing: ListingDetailResponseDTO
  isOwner: boolean
  canApprove: boolean
  isAdminOrApprover: boolean
  onDeposit: () => void
  onClosure: () => void
  onCancellation: () => void
  onSoldOut: () => void
  onApprove: () => void
  onReject: () => void
  onDelete: () => void
  onBlockedAction: (action: "edit" | "delete") => void
  onSubmitForApproval?: () => void
  isSubmitting?: boolean
  isDeleting?: boolean
}

export function DealActionButtons({
  listing,
  isOwner,
  canApprove,
  isAdminOrApprover,
  onDeposit,
  onClosure,
  onCancellation,
  onSoldOut,
  onApprove,
  onReject,
  onDelete,
  onBlockedAction,
  onSubmitForApproval,
  isSubmitting,
  isDeleting,
}: DealActionButtonsProps) {
  const isConHang = listing.status === "CON_HANG"
  const isDaCoc = listing.status === "DA_COC"
  const isDraft = listing.status === "DRAFT"
  const isPendingApproval = listing.status === "PENDING_APPROVAL"
  const isBlocked = BLOCKED_STATUSES.includes(listing.status)

  const showEdit = isOwner || isAdminOrApprover
  const showDelete = isAdminOrApprover

  const handleDelete = () => {
    if (isBlocked) {
      onBlockedAction("delete")
      return
    }
    onDelete()
  }

  return (
    <div className="space-y-3">
      {showEdit && (
        <Link
          to={`/tin/${listing.id}/chinh-sua`}
          onClick={(e) => {
            if (isBlocked) {
              e.preventDefault()
              onBlockedAction("edit")
            }
          }}
        >
          <Button variant="outline" className="w-full gap-2">
            <Pencil className="h-4 w-4" />
            Chỉnh sửa lại thông tin hàng
          </Button>
        </Link>
      )}

      {isOwner && isDraft && (
        <Button
          variant="default"
          className="w-full gap-2"
          onClick={onSubmitForApproval}
          disabled={isSubmitting}
        >
          {isSubmitting ? "Đang gửi..." : "Đăng tin"}
        </Button>
      )}

      {showDelete && (
        <Button
          variant="outline"
          className="w-full gap-2 text-destructive hover:text-destructive"
          onClick={handleDelete}
          disabled={isDeleting}
        >
          <Trash2 className="h-4 w-4" />
          {isDeleting ? "Đang xoá..." : "Xoá tin"}
        </Button>
      )}

      {canApprove && isPendingApproval && (
        <div className="grid grid-cols-2 gap-2">
          <Button variant="default" onClick={onApprove}>
            Duyệt
          </Button>
          <Button variant="destructive" onClick={onReject}>
            Từ chối
          </Button>
        </div>
      )}

      <div className="grid grid-cols-2 gap-2">
        <Button
          variant="default"
          disabled={!isConHang}
          onClick={onDeposit}
        >
          Báo khách cọc
        </Button>
        <Button
          variant="secondary"
          disabled={!isConHang}
          onClick={onSoldOut}
        >
          Báo hết hàng
        </Button>
        <Button
          variant="outline"
          disabled={!isDaCoc}
          onClick={onClosure}
        >
          Báo khách chốt hàng
        </Button>
        <Button
          variant="outline"
          disabled={!isDaCoc}
          onClick={onCancellation}
        >
          Báo khách huỷ cọc
        </Button>
      </div>

      <div className="flex gap-2">
        <Button variant="ghost" size="icon" className="flex-1 gap-1" onClick={() => {}}>
          <Heart className="h-4 w-4" /> Yêu thích
        </Button>
        <Button variant="ghost" size="icon" className="flex-1 gap-1" onClick={() => {}}>
          <Share2 className="h-4 w-4" /> Chia sẻ
        </Button>
      </div>
    </div>
  )
}
