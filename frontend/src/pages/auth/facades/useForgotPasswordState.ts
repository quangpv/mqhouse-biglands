import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import type { IForgotPasswordForm } from "../types"

const forgotPasswordSchema = z.object({
  username: z.string().min(1, "Vui lòng nhập tên đăng nhập"),
})

export function useForgotPasswordState() {
  const form = useForm<IForgotPasswordForm>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: { username: "" },
    mode: "onSubmit",
  })

  return { form, forgotPasswordSchema }
}
