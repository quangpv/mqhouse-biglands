import { Navigate } from "react-router-dom"
import { useAuthStore } from "@/shared/context/auth-store"

interface RoleGuardProps {
  children: React.ReactNode
  roles: string[]
  fallback?: React.ReactNode
}

export function RoleGuard({ children, roles, fallback }: RoleGuardProps) {
  const user = useAuthStore((s) => s.user)

  if (!user || !roles.includes(user.role)) {
    if (fallback) return <>{fallback}</>
    return <Navigate to="/403" replace />
  }

  return <>{children}</>
}
