import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import type { ILoginForm } from "../types"

const loginSchema = z.object({
  username: z.string().min(1, "Vui lòng nhập tên đăng nhập"),
  password: z.string().min(8, "Mật khẩu ít nhất 8 ký tự"),
})

export function useLoginState() {
  const form = useForm<ILoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { username: "", password: "" },
    mode: "onSubmit",
  })

  return { form, loginSchema }
}
