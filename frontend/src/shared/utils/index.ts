export { formatPrice } from "./format"
export type { FormatOptions } from "./format"

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  })
}

export function formatDateTime(date: string): string {
  return new Date(date).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function formatArea(area: number): string {
  return `${area} m²`
}

export function formatPhone(phone: string | null): string {
  if (!phone) return ""
  const s = phone.replace(/\D/g, "")
  if (s.length === 10) return `${s.slice(0, 3)} ${s.slice(3, 6)} ${s.slice(6)}`
  return phone
}

export function getStatusColor(status: string): string {
  const map: Record<string, string> = {
    DRAFT: "bg-gray-500",
    PENDING_APPROVAL: "bg-yellow-500",
    CON_HANG: "bg-green-500",
    DA_COC: "bg-blue-500",
    HET_HANG: "bg-red-500",
    DA_CHOT: "bg-purple-500",
    HUY_COC: "bg-orange-500",
    QUA_HAN: "bg-red-800",
  }
  return map[status] || "bg-gray-400"
}

export function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    DRAFT: "Nháp",
    PENDING_APPROVAL: "Chờ duyệt",
    CON_HANG: "Còn hàng",
    DA_COC: "Đã cọc",
    HET_HANG: "Hết hàng",
    DA_CHOT: "Đã chốt",
    HUY_COC: "Huỷ cọc",
    QUA_HAN: "Quá hạn",
  }
  return map[status] || status
}

export function getTransactionTypeLabel(type: string): string {
  const map: Record<string, string> = {
    BAN: "Bán",
    CHO_THUE: "Cho thuê",
    SANG_NHUONG: "Sang nhượng",
  }
  return map[type] || type
}

export function getPropertyTypeLabel(type: string): string {
  const map: Record<string, string> = {
    NHA_PHO: "Nhà phố",
    CAN_HO: "Căn hộ",
    CHDV: "CHDV",
    DAT: "Đất",
    BIET_THU: "Biệt thự",
    VAN_PHONG: "Văn phòng",
    MAT_BANG: "Mặt bằng",
    KHO_XUONG: "Kho xưởng",
    NHA_TRO: "Nhà trọ",
    KHAC: "Khác",
  }
  return map[type] || type
}

export function getQueueTypeLabel(type: string): string {
  const map: Record<string, string> = {
    "listing-post": "Đăng tin",
    deposit: "Cọc",
    closure: "Tất toán",
    cancellation: "Huỷ cọc",
    "sold-out": "Hết hàng",
  }
  return map[type] || type
}
