export interface IListing {
  id: string
  code: string
  transaction_type: string
  title: string | null
  price: number
  total_area: number
  price_per_m2: number | null
  area_width: number
  area_length: number
  num_rooms: number
  num_bathrooms: number
  num_floors: number
  street_name: string
  ward: string
  district: string
  city: string
  address: string
  status: string
  is_hot: boolean
  is_pinned: boolean
  hot_order: number | null
  primary_image_url: string | null
  created_by_id: string
  creator: { full_name: string } | null
  created_at: string
}
