import { Button } from "@/shared/components/ui/button"
import { Heart, Share2, Pencil } from "lucide-react"
import { Link } from "react-router-dom"
import type { ListingDetailResponseDTO } from "@/data/types/listing.dto"

interface DealActionButtonsProps {
  listing: ListingDetailResponseDTO
  isOwner: boolean
  onDeposit: () => void
  onClosure: () => void
  onCancellation: () => void
  onSoldOut: () => void
  onSubmitForApproval?: () => void
  isSubmitting?: boolean
}

export function DealActionButtons({
  listing,
  isOwner,
  onDeposit,
  onClosure,
  onCancellation,
  onSoldOut,
  onSubmitForApproval,
  isSubmitting,
}: DealActionButtonsProps) {
  const isConHang = listing.status === "CON_HANG"
  const isDaCoc = listing.status === "DA_COC"
  const isDraft = listing.status === "DRAFT"

  return (
    <div className="space-y-3">
      {isOwner && (
        <Link to={`/tin/${listing.id}/chinh-sua`}>
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
