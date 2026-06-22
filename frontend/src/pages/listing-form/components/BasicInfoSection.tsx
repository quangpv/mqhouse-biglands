import type { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import type { IListingForm } from "../types"

interface Props {
  form: UseFormReturn<IListingForm>
  disabled?: boolean
  isEdit?: boolean
}

const TRANSACTION_LABELS: Record<string, string> = {
  BAN: "Bán",
  CHO_THUE: "Cho thuê",
  SANG_NHUONG: "Sang nhượng",
}

const PROPERTY_LABELS: Record<string, string> = {
  CHDV: "Căn hộ chung cư",
  NHA_O: "Nhà ở",
  DAT_NEN: "Đất nền",
  CAO_OC: "Cao ốc",
  KHU_DO_THI: "Khu đô thị",
  KHO_XUONG: "Kho - Xưởng",
  PHONG_TRO: "Phòng trọ",
  VAN_PHONG: "Văn phòng",
  MAT_BANG: "Mặt bằng",
  NHA_TRO: "Nhà trọ",
  BIET_THU: "Biệt thự",
  CONDO_TEL: "Condo-tel",
  SHOPHOUSE: "Shophouse",
  RESORT: "Resort",
  RUNG_TRANG_TRAI: "Rừng - Trang trại",
}

export function BasicInfoSection({ form, disabled }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Thông tin cơ bản</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <FormField
          control={form.control}
          name="transactionType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Loại giao dịch</FormLabel>
              <FormControl>
                <select
                  className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                  {...field}
                  disabled={disabled}
                >
                  {Object.entries(TRANSACTION_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="propertyType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Loại bất động sản</FormLabel>
              <FormControl>
                <select
                  className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                  {...field}
                  disabled={disabled}
                >
                  <option value="">Chọn loại BĐS</option>
                  {Object.entries(PROPERTY_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tiêu đề (không bắt buộc)</FormLabel>
              <FormControl>
                <Input {...field} placeholder="Nhập tiêu đề tin đăng" disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Mô tả chi tiết</FormLabel>
              <FormControl>
                <textarea
                  className="min-h-[120px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                  {...field}
                  placeholder="Nhập mô tả chi tiết về bất động sản"
                  disabled={disabled}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </CardContent>
    </Card>
  )
}
