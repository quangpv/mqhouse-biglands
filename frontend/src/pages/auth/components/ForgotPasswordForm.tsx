import { Link } from "react-router-dom"
import type { UseFormReturn } from "react-hook-form"
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/shared/components/ui/form"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import type { IForgotPasswordForm } from "../types"

interface ForgotPasswordFormProps {
  form: UseFormReturn<IForgotPasswordForm>
  onSubmit: (data: IForgotPasswordForm) => void
  isPending: boolean
  error?: string
}

export function ForgotPasswordForm({ form, onSubmit, isPending, error }: ForgotPasswordFormProps) {
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tên đăng nhập</FormLabel>
              <FormControl>
                <Input placeholder="Tên đăng nhập" autoComplete="username" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {error && (
          <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
            {error}
          </div>
        )}

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? "Đang xử lý..." : "Gửi yêu cầu"}
        </Button>

        <div className="text-center">
          <Link to="/dang-nhap" className="text-sm text-primary hover:underline">
            Quay lại đăng nhập
          </Link>
        </div>
      </form>
    </Form>
  )
}
