import { Navigate, useLocation } from "react-router-dom"
import { useAuthContext } from "@/shared/context/auth-context"
import { useAuthStore } from "@/shared/context/auth-store"
import { LoadingScreen } from "./loading-screen"

interface AuthGuardProps {
  children: React.ReactNode
  roles?: string[]
}

export function AuthGuard({ children, roles }: AuthGuardProps) {
  const { isAuthenticated, isLoading } = useAuthContext()
  const user = useAuthStore((s) => s.user)
  const location = useLocation()

  if (isLoading) return <LoadingScreen />

  if (!isAuthenticated) {
    return <Navigate to="/dang-nhap" state={{ from: location }} replace />
  }

  if (roles && user && !roles.includes(user.role)) {
    return <Navigate to="/403" replace />
  }

  return <>{children}</>
}
