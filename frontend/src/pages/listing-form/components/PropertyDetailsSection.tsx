import type { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import type { IListingForm } from "../types"

interface Props {
  form: UseFormReturn<IListingForm>
  disabled?: boolean
  onAreaChange?: () => void
}

const FURNISHING_LABELS: Record<string, string> = {
  DAY_DU: "Đầy đủ",
  CAO_CAP: "Cao cấp",
  CO_BAN: "Cơ bản",
  CHUA_NOI_THAT: "Chưa có nội thất",
  KHONG: "Không",
}

const FRONTAGE_LABELS: Record<string, string> = {
  MAT_TIEN: "Mặt tiền",
  TRONG_HEM: "Trong hẻm",
  KHONG: "Không",
}

const LEGAL_LABELS: Record<string, string> = {
  SO_HONG: "Sổ hồng",
  SO_DO: "Sổ đỏ",
  CHUA_SO: "Chưa có sổ",
  HOP_DONG: "Hợp đồng",
}

const DIRECTION_LABELS: Record<string, string> = {
  DONG: "Đông",
  TAY: "Tây",
  NAM: "Nam",
  BAC: "Bắc",
  DONG_BAC: "Đông Bắc",
  DONG_NAM: "Đông Nam",
  TAY_BAC: "Tây Bắc",
  TAY_NAM: "Tây Nam",
}

export function PropertyDetailsSection({ form, disabled, onAreaChange }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Thông tin chi tiết</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="areaWidth"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Chiều ngang (m)</FormLabel>
                <FormControl>
                  <Input type="number" step="0.01" {...field} disabled={disabled} onChange={(e) => { field.onChange(e); onAreaChange?.() }} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="areaLength"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Chiều dài (m)</FormLabel>
                <FormControl>
                  <Input type="number" step="0.01" {...field} disabled={disabled} onChange={(e) => { field.onChange(e); onAreaChange?.() }} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="totalArea"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tổng diện tích (m²)</FormLabel>
                <FormControl>
                  <Input type="number" step="0.01" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="numRooms"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Số phòng ngủ</FormLabel>
                <FormControl>
                  <Input type="number" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="numBathrooms"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Số phòng tắm</FormLabel>
                <FormControl>
                  <Input type="number" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="numFloors"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Số tầng</FormLabel>
                <FormControl>
                  <Input type="number" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="furnishing"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Nội thất</FormLabel>
                <FormControl>
                  <select
                    className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                    {...field}
                    disabled={disabled}
                  >
                    <option value="">Chọn tình trạng</option>
                    {Object.entries(FURNISHING_LABELS).map(([v, l]) => (
                      <option key={v} value={v}>{l}</option>
                    ))}
                  </select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="frontageType"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Loại mặt tiền</FormLabel>
                <FormControl>
                  <select
                    className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                    {...field}
                    disabled={disabled}
                  >
                    <option value="">Chọn loại</option>
                    {Object.entries(FRONTAGE_LABELS).map(([v, l]) => (
                      <option key={v} value={v}>{l}</option>
                    ))}
                  </select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="legalStatus"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tình trạng pháp lý</FormLabel>
                <FormControl>
                  <select
                    className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                    {...field}
                    disabled={disabled}
                  >
                    <option value="">Chọn tình trạng</option>
                    {Object.entries(LEGAL_LABELS).map(([v, l]) => (
                      <option key={v} value={v}>{l}</option>
                    ))}
                  </select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="direction"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Hướng</FormLabel>
                <FormControl>
                  <select
                    className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                    {...field}
                    disabled={disabled}
                  >
                    <option value="">Chọn hướng</option>
                    {Object.entries(DIRECTION_LABELS).map(([v, l]) => (
                      <option key={v} value={v}>{l}</option>
                    ))}
                  </select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="roadWidth"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Đường rộng</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="VD: 5m, 10m" disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="label"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nhãn (không bắt buộc)</FormLabel>
              <FormControl>
                <Input {...field} placeholder="VD: Góc 2 mặt tiền, View đẹp..." disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </CardContent>
    </Card>
  )
}
