import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate, useLocation } from "react-router-dom"
import { authRepository } from "@/data/repositories/auth.repository"
import { authQueries } from "@/data/queries/auth.queries"
import { useAuthStore } from "@/shared/context/auth-store"
import { useToast } from "@/shared/context/toast-provider"
import type { ILoginForm } from "../types"

export function useLogin() {
  const setAuth = useAuthStore((s) => s.setAuth)
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const location = useLocation()
  const { showError } = useToast()

  return useMutation({
    mutationFn: (data: ILoginForm) => authRepository.login(data),
    onSuccess: (res) => {
      setAuth(res.token, res.user)
      queryClient.setQueryData(authQueries.me, res.user)
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname
      navigate(from || "/", { replace: true })
    },
    onError: (err) => showError(err),
  })
}
