import httpClient from "../infra/http-client"
import type { DealEventDTO } from "../types/listing.dto"

export interface ReportDepositPayload {
  customerName: string
  customerPhone?: string
  depositAmount: number
  notes?: string
}

export interface ReportClosurePayload {
  notes?: string
}

export interface ReportCancellationPayload {
  notes: string
}

export interface ReportSoldOutPayload {
  notes?: string
}

export const dealEventRepository = {
  reportDeposit: (listingId: string, data: ReportDepositPayload) =>
    httpClient.post<DealEventDTO>(`/listings/${listingId}/deal-events/deposit`, data).then((r) => r.data),

  reportClosure: (listingId: string, data: ReportClosurePayload) =>
    httpClient.post<DealEventDTO>(`/listings/${listingId}/deal-events/closure`, data).then((r) => r.data),

  reportCancellation: (listingId: string, data: ReportCancellationPayload) =>
    httpClient.post<DealEventDTO>(`/listings/${listingId}/deal-events/cancellation`, data).then((r) => r.data),

  reportSoldOut: (listingId: string, data: ReportSoldOutPayload) =>
    httpClient.post<DealEventDTO>(`/listings/${listingId}/deal-events/sold-out`, data).then((r) => r.data),
}
