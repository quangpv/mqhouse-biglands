import { FormProvider } from "react-hook-form"
import type { UseFormReturn } from "react-hook-form"
import { Card } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Label } from "@/shared/components/ui/label"
import { Switch } from "@/shared/components/ui/switch"
import { Select } from "@/shared/components/ui/select"
import { Controller } from "react-hook-form"
import type { IUserFormData } from "../types"

interface UserFormProps {
  form: UseFormReturn<IUserFormData>
  mode: "create" | "edit"
  onSubmit: (data: IUserFormData) => void
  isPending: boolean
}

export function UserForm({ form, mode, onSubmit, isPending }: UserFormProps) {
  return (
    <FormProvider {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card className="p-6 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="fullName">Họ tên *</Label>
            <Input id="fullName" {...form.register("fullName")} placeholder="Nhập họ tên" />
            {form.formState.errors.fullName && (
              <p className="text-xs text-destructive">{form.formState.errors.fullName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="username">Tên đăng nhập *</Label>
            <Input id="username" {...form.register("username")} placeholder="Nhập tên đăng nhập" disabled={mode === "edit"} />
            {form.formState.errors.username && (
              <p className="text-xs text-destructive">{form.formState.errors.username.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">Số điện thoại</Label>
            <Input id="phone" {...form.register("phone")} placeholder="Nhập số điện thoại" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" {...form.register("email")} placeholder="Nhập email" />
            {form.formState.errors.email && (
              <p className="text-xs text-destructive">{form.formState.errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="role">Vai trò *</Label>
            <Controller
              name="role"
              control={form.control}
              render={({ field }) => (
                <Select
                  value={field.value}
                  onValueChange={field.onChange}
                  options={[
                    { value: "AGENT", label: "Môi giới" },
                    { value: "APPROVER", label: "Người duyệt" },
                    { value: "ADMIN", label: "Quản trị viên" },
                  ]}
                />
              )}
            />
          </div>

          {mode === "create" && (
            <div className="space-y-2">
              <Label htmlFor="password">Mật khẩu (để trống để tự động tạo)</Label>
              <Input id="password" type="password" {...form.register("password")} placeholder="Nhập mật khẩu hoặc để trống" />
              {form.formState.errors.password && (
                <p className="text-xs text-destructive">{form.formState.errors.password.message}</p>
              )}
            </div>
          )}

          {mode === "edit" && (
            <div className="flex items-center gap-3">
              <Label htmlFor="isActive">Trạng thái hoạt động</Label>
              <Controller
                name="isActive"
                control={form.control}
                render={({ field }) => (
                  <Switch checked={field.value} onCheckedChange={field.onChange} />
                )}
              />
            </div>
          )}
        </Card>

        <div className="flex justify-end gap-3">
          <Button variant="outline" type="button" onClick={() => window.history.back()}>
            Huỷ
          </Button>
          <Button type="submit" disabled={isPending}>
            {isPending ? "Đang lưu..." : mode === "create" ? "Tạo người dùng" : "Lưu thay đổi"}
          </Button>
        </div>
      </form>
    </FormProvider>
  )
}
