import type { PaginationDTO } from "./common.dto"

export interface ListingDTO {
  id: string
  code: string
  transactionType: "BAN" | "CHO_THUE" | "SANG_NHUONG"
  propertyType: string
  title: string | null
  description: string
  price: number
  commissionType: "PERCENTAGE" | "FLAT"
  commissionValue: number
  areaWidth: number
  areaLength: number
  totalArea: number
  numRooms: number
  numBathrooms: number
  numFloors: number
  streetName: string
  houseNumber: string
  address: string
  ward: string
  district: string
  city: string
  latitude: number | null
  longitude: number | null
  label: string | null
  furnishing: string | null
  frontageType: string | null
  legalStatus: string | null
  direction: string | null
  roadWidth: string | null
  ownerPhone: string | null
  videoUrl: string | null
  status: ListingStatus
  isHot: boolean
  hotOrder: number | null
  viewCount: number
  pricePerM2: number | null
  requiresApproval: boolean
  createdById: string
  creatorInfo: CreatorInfoDTO | null
  approvedById: string | null
  approvedAt: string | null
  createdAt: string
  updatedAt: string
}

export type ListingStatus =
  | "DRAFT"
  | "PENDING_APPROVAL"
  | "CON_HANG"
  | "DA_COC"
  | "HET_HANG"
  | "DA_CHOT"
  | "HUY_COC"
  | "QUA_HAN"

export interface CreatorInfoDTO {
  id: string
  fullName: string
  username: string
  phone: string | null
}

export interface ListingImageDTO {
  id: string
  listingId: string
  url: string
  order: number
  isPrimary: boolean
}

export interface DealEventDTO {
  id: string
  listingId: string
  eventType: string
  reportedById: string
  confirmedById: string | null
  confirmedAt: string | null
  notes: string | null
  customerName: string | null
  customerPhone: string | null
  depositAmount: number | null
  createdAt: string
}

export interface ListingDetailResponseDTO {
  listing: ListingDTO
  images: ListingImageDTO[]
  dealEvents: DealEventDTO[]
  isPinned: boolean
}

export interface FilterCountsDTO {
  conHang: number
  daCoc: number
  tatToan: number
}

export interface ListingListResponseDTO {
  data: ListingDTO[]
  pagination: PaginationDTO
  filterCounts: FilterCountsDTO
  totalCount: number
}
