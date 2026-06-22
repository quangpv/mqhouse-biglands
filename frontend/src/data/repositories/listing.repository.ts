import httpClient from "../infra/http-client"
import type { ListingListResponseDTO, ListingDetailResponseDTO } from "../types/listing.dto"

export interface ListingListParams {
  page?: number
  size?: number
  q?: string
  transactionType?: string
  status?: string[]
  createdBy?: string
  isHot?: boolean
  filter?: string
  sortBy?: string
  sortOrder?: string
}

export const listingRepository = {
  list: (params?: ListingListParams) =>
    httpClient.get<ListingListResponseDTO>("/listings", { params }).then((r) => r.data),

  getHotListings: (params?: ListingListParams) =>
    httpClient.get<ListingListResponseDTO>("/listings", { params: { ...params, isHot: true } }).then((r) => r.data),

  getMyPins: (params?: ListingListParams) =>
    httpClient.get<ListingListResponseDTO>("/listings", { params: { ...params, filter: "pinned" } }).then((r) => r.data),

  get: (id: string) =>
    httpClient.get<ListingDetailResponseDTO>(`/listings/${id}`).then((r) => r.data),

  create: (data: Record<string, unknown>) =>
    httpClient.post("/listings", data).then((r) => r.data),

  update: (id: string, data: Record<string, unknown>) =>
    httpClient.put(`/listings/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    httpClient.delete(`/listings/${id}`).then(() => undefined),

  submit: (id: string) =>
    httpClient.post(`/listings/${id}/submit`).then((r) => r.data),

  withdraw: (id: string) =>
    httpClient.post(`/listings/${id}/withdraw`).then((r) => r.data),

  pin: (id: string) =>
    httpClient.put(`/listings/${id}/pin`).then((r) => r.data),

  unpin: (id: string) =>
    httpClient.delete(`/listings/${id}/pin`).then(() => undefined),

  uploadImage: (id: string, formData: FormData) =>
    httpClient.post(`/listings/${id}/images`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }).then((r) => r.data),

  promoteToHot: (id: string, hotOrder: number) =>
    httpClient.post(`/listings/${id}/promote`, { hotOrder }).then((r) => r.data),

  unpromoteFromHot: (id: string) =>
    httpClient.delete(`/listings/${id}/promote`).then((r) => r.data),

  reorderHotListings: (order: Array<{ listingId: string; hotOrder: number }>) =>
    httpClient.put("/hot-listings/reorder", { order }).then((r) => r.data),
}
