import type { ListingDTO } from "@/data/types/listing.dto"
import type { IListing } from "@/shared/types/listing.type"

export function dtoToIListing(dto: ListingDTO): IListing {
  return {
    id: dto.id,
    code: dto.code,
    transaction_type: dto.transaction_type,
    title: dto.title,
    price: dto.price,
    total_area: dto.total_area,
    price_per_m2: dto.price_per_m2,
    area_width: dto.area_width,
    area_length: dto.area_length,
    num_rooms: dto.num_rooms,
    num_bathrooms: dto.num_bathrooms,
    num_floors: dto.num_floors,
    street_name: dto.street_name,
    ward: dto.ward,
    district: dto.district,
    city: dto.city,
    address: dto.address,
    status: dto.status,
    is_hot: dto.is_hot,
    is_pinned: dto.is_pinned,
    hot_order: dto.hot_order,
    primary_image_url: dto.primary_image_url,
    created_by_id: dto.created_by_id,
    creator: dto.creator ? { full_name: dto.creator.full_name } : null,
    created_at: dto.created_at,
  }
}
