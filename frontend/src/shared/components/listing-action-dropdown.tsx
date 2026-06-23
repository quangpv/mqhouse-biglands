import { MoreVertical, Check, X, Pencil, Trash2, Flame, ArrowLeftFromLine } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/shared/components/ui/dropdown-menu"
import type { IListing } from "@/shared/types/listing.type"
import type { UserDTO } from "@/data/types/auth.dto"

const BLOCKED_STATUSES = ["DA_COC", "DA_CHOT", "HET_HANG", "HUY_COC", "QUA_HAN"]

interface ListingActionDropdownProps {
  listing: IListing
  user: UserDTO | null
  onApprove: (listing: IListing) => void
  onReject: (listing: IListing) => void
  onEdit: (listing: IListing) => void
  onDelete: (listing: IListing) => void
  onWithdraw?: (listing: IListing) => void
  onBlockedAction: (listing: IListing, action: "edit" | "delete") => void
  onPromoteToHot: (listing: IListing) => void
  onUnpromoteFromHot: (listing: IListing) => void
}

export function ListingActionDropdown({
  listing,
  user,
  onApprove,
  onReject,
  onEdit,
  onDelete,
  onWithdraw,
  onBlockedAction,
  onPromoteToHot,
  onUnpromoteFromHot,
}: ListingActionDropdownProps) {
  const isAdmin = user?.role === "ADMIN"
  const isAdminOrApprover = isAdmin || user?.role === "APPROVER"
  const isOwner = user?.id === listing.created_by_id
  const isBlocked = BLOCKED_STATUSES.includes(listing.status)
  const isPendingApproval = listing.status === "PENDING_APPROVAL"

  const canEditInStatus = ["DRAFT", "PENDING_APPROVAL", "CON_HANG"].includes(listing.status)

  const showApproveReject = isPendingApproval && isAdminOrApprover
  const showEditButton = isAdminOrApprover || (isOwner && canEditInStatus)
  const showDeleteButton = isAdminOrApprover || (isOwner && listing.status === "DRAFT")
  const showWithdraw = isOwner && listing.status === "CON_HANG" && !!onWithdraw
  const showPromoteHot = isAdmin && !listing.is_hot
  const showUnpromoteHot = isAdmin && listing.is_hot

  const hasAnyAction = showApproveReject || showEditButton || showDeleteButton || showWithdraw || showPromoteHot || showUnpromoteHot
  if (!hasAnyAction) return null

  const handleEdit = () => {
    if (isBlocked) {
      onBlockedAction(listing, "edit")
      return
    }
    onEdit(listing)
  }

  const handleDelete = () => {
    if (isBlocked) {
      onBlockedAction(listing, "delete")
      return
    }
    onDelete(listing)
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
          }}
          className="flex h-7 w-7 items-center justify-center rounded-full bg-white/80 shadow-sm hover:bg-white transition-colors"
          aria-label="Thao tác"
        >
          <MoreVertical className="h-4 w-4 text-gray-600" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-[160px]">
        {showApproveReject && (
          <>
            <DropdownMenuItem
              onClick={(e) => { e.stopPropagation(); onApprove(listing) }}
            >
              <Check className="h-4 w-4 mr-2 text-green-600" />
              Duyệt
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={(e) => { e.stopPropagation(); onReject(listing) }}
            >
              <X className="h-4 w-4 mr-2 text-red-600" />
              Từ chối
            </DropdownMenuItem>
          </>
        )}

        {(showPromoteHot || showUnpromoteHot) && (
          <>
            {(showApproveReject) && <DropdownMenuSeparator />}
            {showPromoteHot && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); onPromoteToHot(listing) }}
              >
                <Flame className="h-4 w-4 mr-2 text-orange-500" />
                Ghim hot
              </DropdownMenuItem>
            )}
            {showUnpromoteHot && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); onUnpromoteFromHot(listing) }}
              >
                <Flame className="h-4 w-4 mr-2 text-gray-500" />
                Bỏ ghim hot
              </DropdownMenuItem>
            )}
          </>
        )}

        {(showEditButton || showWithdraw || showDeleteButton) && (
          <>
            {(showApproveReject || showPromoteHot || showUnpromoteHot) && <DropdownMenuSeparator />}
            {showEditButton && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); handleEdit() }}
              >
                <Pencil className="h-4 w-4 mr-2" />
                Sửa
              </DropdownMenuItem>
            )}
            {showWithdraw && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); onWithdraw?.(listing) }}
              >
                <ArrowLeftFromLine className="h-4 w-4 mr-2" />
                Rút tin
              </DropdownMenuItem>
            )}
            {showDeleteButton && (
              <DropdownMenuItem
                variant="destructive"
                onClick={(e) => { e.stopPropagation(); handleDelete() }}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Xoá
              </DropdownMenuItem>
            )}
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
