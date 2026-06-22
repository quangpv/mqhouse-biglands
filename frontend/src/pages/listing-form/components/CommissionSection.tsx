import { useWatch } from "react-hook-form"
import type { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import type { IListingForm } from "../types"

interface Props {
  form: UseFormReturn<IListingForm>
  disabled?: boolean
}

export function CommissionSection({ form, disabled }: Props) {
  const [transactionType, commissionType] = useWatch({
    control: form.control,
    name: ["transactionType", "commissionType"],
  })

  const commissionPlaceholder = commissionType === "PERCENTAGE" ? "VD: 1.5" : "VD: 50000000"

  return (
    <Card>
      <CardHeader>
        <CardTitle>Giá và hoa hồng</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <FormField
          control={form.control}
          name="price"
          render={({ field }) => (
            <FormItem>
              <FormLabel>
                Giá {transactionType === "CHO_THUE" ? "thuê (VNĐ/tháng)" : "bán (VNĐ)"}
              </FormLabel>
              <FormControl>
                <Input type="number" step="1000000" {...field} disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="commissionType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Loại hoa hồng</FormLabel>
              <FormControl>
                <select
                  className="h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50"
                  {...field}
                  disabled={disabled}
                >
                  <option value="PERCENTAGE">Phần trăm (%)</option>
                  <option value="FLAT">Số tiền cố định (VNĐ)</option>
                </select>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="commissionValue"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Giá trị hoa hồng</FormLabel>
              <FormControl>
                <Input type="number" step="any" {...field} placeholder={commissionPlaceholder} disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </CardContent>
    </Card>
  )
}
