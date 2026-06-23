import type { PaginationDTO } from "./common.dto"

export interface ListingDTO {
  id: string
  code: string
  transaction_type: "BAN" | "CHO_THUE" | "SANG_NHUONG"
  property_type: string
  title: string | null
  description: string
  price: number
  commission_type: "PERCENTAGE" | "FLAT"
  commission_value: number
  area_width: number
  area_length: number
  total_area: number
  num_rooms: number
  num_bathrooms: number
  num_floors: number
  street_name: string
  house_number: string
  address: string
  ward: string
  district: string
  city: string
  latitude: number | null
  longitude: number | null
  label: string | null
  furnishing: string | null
  frontage_type: string | null
  legal_status: string | null
  direction: string | null
  road_width: string | null
  owner_phone: string | null
  video_url: string | null
  status: ListingStatus
  is_hot: boolean
  is_pinned: boolean
  hot_order: number | null
  view_count: number
  price_per_m2: number | null
  primary_image_url: string | null
  requires_approval: boolean
  created_by_id: string
  creator: CreatorInfoDTO | null
  approved_by_id: string | null
  approved_at: string | null
  created_at: string
  updated_at: string
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
  full_name: string
  username: string
  phone: string | null
}

export interface ListingImageDTO {
  id: string
  listing_id: string
  url: string
  order: number
  is_primary: boolean
}

export interface DealEventDTO {
  id: string
  listing_id: string
  event_type: string
  reported_by_id: string
  confirmed_by_id: string | null
  confirmed_at: string | null
  notes: string | null
  customer_name: string | null
  customer_phone: string | null
  deposit_amount: number | null
  created_at: string
}

export interface ListingDetailResponseDTO extends ListingDTO {
  images: ListingImageDTO[]
  deal_events: DealEventDTO[]
}

export interface FilterCountsDTO {
  all: number
  hot: number
  pinned: number
}

export interface ListingListResponseDTO {
  data: ListingDTO[]
  page: number
  size: number
  total: number
  total_pages: number
  total_count: number
}
