import { z } from "zod"
import type { ListingDTO } from "@/data/types/listing.dto"

export const listingFormSchema = z.object({
  transactionType: z.enum(["BAN", "CHO_THUE", "SANG_NHUONG"]),
  propertyType: z.string().min(1, "Vui lòng chọn loại bất động sản"),
  title: z.string().max(500).optional(),
  description: z.string().min(1, "Vui lòng nhập mô tả"),
  price: z.coerce.number({ message: "Vui lòng nhập giá" }).positive("Giá phải lớn hơn 0"),
  commissionType: z.enum(["PERCENTAGE", "FLAT"]),
  commissionValue: z.coerce.number({ message: "Vui lòng nhập giá trị hoa hồng" }).nonnegative("Giá trị không âm"),
  areaWidth: z.coerce.number({ message: "Vui lòng nhập chiều ngang" }).positive("Chiều ngang phải lớn hơn 0"),
  areaLength: z.coerce.number({ message: "Vui lòng nhập chiều dài" }).positive("Chiều dài phải lớn hơn 0"),
  totalArea: z.coerce.number({ message: "Vui lòng nhập tổng diện tích" }).positive("Diện tích phải lớn hơn 0"),
  numRooms: z.coerce.number().int().nonnegative().optional(),
  numBathrooms: z.coerce.number().int().nonnegative().optional(),
  numFloors: z.coerce.number().int().nonnegative().optional(),
  streetName: z.string().min(1, "Vui lòng nhập tên đường"),
  houseNumber: z.string().min(1, "Vui lòng nhập số nhà"),
  address: z.string().min(1, "Vui lòng nhập địa chỉ"),
  ward: z.string().min(1, "Vui lòng chọn phường"),
  district: z.string().min(1, "Vui lòng chọn quận"),
  city: z.string().min(1, "Vui lòng chọn thành phố"),
  latitude: z.coerce.number().optional(),
  longitude: z.coerce.number().optional(),
  label: z.string().max(100).optional(),
  furnishing: z.enum(["DAY_DU", "CAO_CAP", "CO_BAN", "CHUA_NOI_THAT", "KHONG"]).optional(),
  frontageType: z.enum(["MAT_TIEN", "TRONG_HEM", "KHONG"]).optional(),
  legalStatus: z.enum(["SO_HONG", "SO_DO", "CHUA_SO", "HOP_DONG"]).optional(),
  direction: z.enum(["DONG", "TAY", "NAM", "BAC", "DONG_BAC", "DONG_NAM", "TAY_BAC", "TAY_NAM"]).optional(),
  roadWidth: z.string().optional(),
  ownerPhone: z.string().min(1, "Vui lòng nhập số điện thoại chủ nhà"),
  videoUrl: z.string().optional(),
  action: z.enum(["draft", "submit"]).optional(),
})

export type IListingForm = z.infer<typeof listingFormSchema>

export interface CreateListingPayload {
  transaction_type: string
  property_type: string
  title: string | null
  description: string
  price: number
  commission_type: string
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
  owner_phone: string
  video_url: string | null
  action: string | null
}

export type UpdateListingPayload = Partial<CreateListingPayload>

export function formToCreatePayload(data: IListingForm): CreateListingPayload {
  return {
    transaction_type: data.transactionType,
    property_type: data.propertyType,
    title: data.title ?? null,
    description: data.description,
    price: data.price,
    commission_type: data.commissionType,
    commission_value: data.commissionValue,
    area_width: data.areaWidth,
    area_length: data.areaLength,
    total_area: data.totalArea,
    num_rooms: data.numRooms ?? 0,
    num_bathrooms: data.numBathrooms ?? 0,
    num_floors: data.numFloors ?? 0,
    street_name: data.streetName,
    house_number: data.houseNumber,
    address: data.address,
    ward: data.ward,
    district: data.district,
    city: data.city,
    latitude: data.latitude ?? null,
    longitude: data.longitude ?? null,
    label: data.label ?? null,
    furnishing: data.furnishing ?? null,
    frontage_type: data.frontageType ?? null,
    legal_status: data.legalStatus ?? null,
    direction: data.direction ?? null,
    road_width: data.roadWidth ?? null,
    owner_phone: data.ownerPhone,
    video_url: data.videoUrl ?? null,
    action: data.action ?? null,
  }
}

export function listingToFormValues(listing: ListingDTO): IListingForm {
  return {
    transactionType: listing.transaction_type,
    propertyType: listing.property_type,
    title: listing.title ?? undefined,
    description: listing.description,
    price: listing.price,
    commissionType: listing.commission_type,
    commissionValue: listing.commission_value,
    areaWidth: listing.area_width,
    areaLength: listing.area_length,
    totalArea: listing.total_area,
    numRooms: listing.num_rooms || undefined,
    numBathrooms: listing.num_bathrooms || undefined,
    numFloors: listing.num_floors || undefined,
    streetName: listing.street_name,
    houseNumber: listing.house_number,
    address: listing.address,
    ward: listing.ward,
    district: listing.district,
    city: listing.city,
    latitude: listing.latitude ?? undefined,
    longitude: listing.longitude ?? undefined,
    label: listing.label ?? undefined,
    furnishing: (listing.furnishing ?? undefined) as IListingForm["furnishing"],
    frontageType: (listing.frontage_type ?? undefined) as IListingForm["frontageType"],
    legalStatus: (listing.legal_status ?? undefined) as IListingForm["legalStatus"],
    direction: (listing.direction ?? undefined) as IListingForm["direction"],
    roadWidth: listing.road_width ?? undefined,
    ownerPhone: listing.owner_phone ?? "",
    videoUrl: listing.video_url ?? undefined,
  }
}
