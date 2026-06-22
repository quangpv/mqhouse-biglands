import type { QueueType, TransactionType } from "../types"

export const queueTypeLabels: Record<QueueType, string> = {
  "listing-post": "Duyệt bài đăng",
  deposit: "Duyệt báo cọc",
  closure: "Duyệt chốt hàng",
  cancellation: "Duyệt huỷ cọc",
  "sold-out": "Duyệt hết hàng",
}

export const transactionTypeLabels: Record<TransactionType, string> = {
  BAN: "Bán",
  CHO_THUE: "Cho thuê",
  SANG_NHUONG: "Sang nhượng",
}

export function getQueueTitle(queueType: QueueType, transactionType?: TransactionType): string {
  const base = queueTypeLabels[queueType] ?? "Duyệt"
  if (transactionType) return `${base} — ${transactionTypeLabels[transactionType]}`
  return base
}
