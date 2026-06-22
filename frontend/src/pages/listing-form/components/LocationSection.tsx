import type { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import { LocationCascade } from "@/shared/components/location-cascade"
import type { IListingForm } from "../types"

interface Props {
  form: UseFormReturn<IListingForm>
  disabled?: boolean
}

export function LocationSection({ form, disabled }: Props) {
  const city = form.watch("city")
  const district = form.watch("district")
  const ward = form.watch("ward")

  return (
    <Card>
      <CardHeader>
        <CardTitle>Địa chỉ</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <LocationCascade
          city={city}
          district={district}
          ward={ward}
          onCityChange={(v) => form.setValue("city", v)}
          onDistrictChange={(v) => form.setValue("district", v)}
          onWardChange={(v) => form.setValue("ward", v)}
          disabled={disabled}
        />

        <div className="grid grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="houseNumber"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Số nhà</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="VD: 123" disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="streetName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tên đường</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="VD: Nguyễn Huệ" disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="address"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Địa chỉ đầy đủ</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="VD: 123 Nguyễn Huệ" disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="latitude"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Vĩ độ (không bắt buộc)</FormLabel>
                <FormControl>
                  <Input type="number" step="any" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="longitude"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Kinh độ (không bắt buộc)</FormLabel>
                <FormControl>
                  <Input type="number" step="any" {...field} disabled={disabled} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
      </CardContent>
    </Card>
  )
}
