import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import type { UserDTO } from "@/data/types/auth.dto"
import type { IUserFormData } from "../types"

const userFormSchema = z.object({
  fullName: z.string().min(1, "Vui lòng nhập họ tên"),
  username: z.string().min(3, "Tên đăng nhập ít nhất 3 ký tự"),
  phone: z.string().optional().default(""),
  email: z.string().email("Email không hợp lệ").optional().or(z.literal("")),
  role: z.enum(["AGENT", "APPROVER", "ADMIN"]),
  password: z.string().min(6, "Mật khẩu ít nhất 6 ký tự").optional().or(z.literal("")),
  isActive: z.boolean().default(true),
})

export function useUserFormState(existingUser?: UserDTO | null) {
  const mode = existingUser ? "edit" : "create"

  const form = useForm<IUserFormData>({
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    resolver: zodResolver(userFormSchema) as any,
    defaultValues: existingUser
      ? {
          fullName: existingUser.full_name,
          username: existingUser.username,
          phone: existingUser.phone ?? "",
          email: existingUser.email ?? "",
          role: existingUser.role,
          password: "",
          isActive: existingUser.is_active,
        }
      : {
          fullName: "",
          username: "",
          phone: "",
          email: "",
          role: "AGENT" as const,
          password: "",
          isActive: true,
        },
  })

  return { form, mode }
}
