import { createContext, useContext, type ReactNode } from "react"
import { toast as sonnerToast } from "sonner"
import { Toaster } from "@/shared/components/ui/sonner"
import { ApiError } from "@/data/infra/api-error"

interface ToastContextValue {
  showError: (error: unknown) => void
  success: (message: string) => string | number
  error: (message: string) => string | number
  info: (message: string) => string | number
  warning: (message: string) => string | number
  loading: (message: string) => string | number
}

const ToastContext = createContext<ToastContextValue | null>(null)

function showError(error: unknown) {
  if (error instanceof ApiError) {
    sonnerToast.error(error.message)
  } else if (import.meta.env.DEV) {
    sonnerToast.error(String(error))
  } else {
    sonnerToast.error("Có lỗi xảy ra")
  }
}

export function ToastProvider({ children }: { children: ReactNode }) {
  return (
    <ToastContext.Provider
      value={{
        showError,
        success: sonnerToast.success,
        error: sonnerToast.error,
        info: sonnerToast.info,
        warning: sonnerToast.warning,
        loading: sonnerToast.loading,
      }}
    >
      {children}
      <Toaster />
    </ToastContext.Provider>
  )
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error("useToast must be used within ToastProvider")
  return ctx
}
