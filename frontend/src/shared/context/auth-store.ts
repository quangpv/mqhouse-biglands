import { create } from "zustand"
import type { UserDTO } from "@/data/types/auth.dto"

interface AuthState {
  token: string | null
  user: UserDTO | null
  setAuth: (token: string, user: UserDTO) => void
  clearAuth: () => void
  isAuthenticated: () => boolean
  hasRole: (...roles: string[]) => boolean
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem("auth-token"),
  user: (() => {
    try {
      const raw = localStorage.getItem("auth-user")
      return raw ? (JSON.parse(raw) as UserDTO) : null
    } catch {
      return null
    }
  })(),

  setAuth: (token: string, user: UserDTO) => {
    localStorage.setItem("auth-token", token)
    localStorage.setItem("auth-user", JSON.stringify(user))
    set({ token, user })
  },

  clearAuth: () => {
    localStorage.removeItem("auth-token")
    localStorage.removeItem("auth-user")
    set({ token: null, user: null })
  },

  isAuthenticated: () => !!get().token,

  hasRole: (...roles: string[]) => {
    const user = get().user
    return !!user && roles.includes(user.role)
  },
}))
