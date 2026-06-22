export interface FormatOptions {
  compact?: boolean
}

export function formatPrice(price: number, options?: FormatOptions): string {
  if (options?.compact) {
    if (price >= 1_000_000_000) return `${(price / 1_000_000_000).toFixed(2)} tỷ`
    if (price >= 1_000_000) return `${(price / 1_000_000).toFixed(0)} tr`
    return price.toLocaleString("vi-VN") + " đ"
  }
  return price.toLocaleString("vi-VN") + " đ"
}
