import type { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import type { IListingForm } from "../types"

interface Props {
  form: UseFormReturn<IListingForm>
  disabled?: boolean
}

export function ContactSection({ form, disabled }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Thông tin liên hệ</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <FormField
          control={form.control}
          name="ownerPhone"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Số điện thoại chủ nhà</FormLabel>
              <FormControl>
                <Input {...field} placeholder="VD: 0901234567" disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="videoUrl"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Video URL (không bắt buộc)</FormLabel>
              <FormControl>
                <Input {...field} placeholder="VD: https://youtube.com/..." disabled={disabled} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </CardContent>
    </Card>
  )
}
