import { formatPhone, formatDate } from "@/shared/utils"
import { Eye, EyeOff } from "lucide-react"
import type { ListingDetailResponseDTO } from "@/data/types/listing.dto"

interface AgentContactInfoProps {
  listing: ListingDetailResponseDTO
  ownerPhoneVisible: boolean
  onToggleOwnerPhone: () => void
}

export function AgentContactInfo({ listing, ownerPhoneVisible, onToggleOwnerPhone }: AgentContactInfoProps) {
  return (
    <div className="space-y-2 rounded-lg border p-4 text-sm">
      <div className="flex items-center justify-between">
        <span className="text-muted-foreground">Người đăng:</span>
        <span className="font-medium">{listing.creatorInfo?.fullName ?? "—"}</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-muted-foreground">Liên hệ:</span>
        <span className="font-medium">{formatPhone(listing.creatorInfo?.phone ?? null) || "—"}</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-muted-foreground">Số điện thoại chủ nhà:</span>
        <button onClick={onToggleOwnerPhone} className="flex items-center gap-1 font-medium hover:underline">
          {ownerPhoneVisible ? (
            <>{formatPhone(listing.ownerPhone)} <EyeOff className="h-3.5 w-3.5 text-muted-foreground" /></>
          ) : (
            <>{listing.ownerPhone ? "Hiện số" : "—"} <Eye className="h-3.5 w-3.5 text-muted-foreground" /></>
          )}
        </button>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-muted-foreground">Ngày đăng:</span>
        <span className="font-medium">{formatDate(listing.createdAt)}</span>
      </div>
    </div>
  )
}
