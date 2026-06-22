import { createContext, useContext, useEffect, type ReactNode } from "react"
import { useQuery } from "@tanstack/react-query"
import { authRepository } from "@/data/repositories/auth.repository"
import { authQueries } from "@/data/queries/auth.queries"
import { useAuthStore } from "./auth-store"

interface AuthContextType {
  isAuthenticated: boolean
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  isLoading: true,
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const { token, user, clearAuth } = useAuthStore()

  const { isLoading } = useQuery({
    queryKey: authQueries.me,
    queryFn: authRepository.me,
    enabled: !!token && !user,
    retry: false,
    meta: { skipAuthRedirect: true },
    gcTime: 0,
  })

  useEffect(() => {
    if (!token) {
      clearAuth()
    }
  }, [token, clearAuth])

  const value: AuthContextType = { isAuthenticated: !!token && !!user, isLoading: !!token && !user && isLoading }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
  return useContext(AuthContext)
}
