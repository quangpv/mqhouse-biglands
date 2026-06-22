import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { QueryClientProvider } from "@tanstack/react-query"
import { queryClient } from "@/data/infra/query-client"
import { AuthProvider, useAuthContext } from "@/shared/context/auth-context"
import { AppLayout } from "@/shared/components/app-layout"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Toaster } from "@/shared/components/ui/sonner"

import {
  LoginPage,
  ForgotPasswordPage,
  ResetPasswordPage,
  HomePage,
  ProductDetailPage,
  CreateListingPage,
  EditListingPage,
  MyCartPage,
  NotificationsPage,
  QueueListPage,
  QueueDetailPage,
  UserListPage,
  CreateUserPage,
  EditUserPage,
  HotProductsPage,
  ForbiddenPage,
  NotFoundPage,
} from "@/pages"

function LoggedInRedirect() {
  const { isAuthenticated, isLoading } = useAuthContext()
  if (isLoading) return null
  if (isAuthenticated) return <Navigate to="/" replace />
  return <LoginPage />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/dang-nhap" element={<LoggedInRedirect />} />
      <Route path="/quen-mat-khau" element={<ForgotPasswordPage />} />
      <Route path="/dat-lai-mat-khau" element={<ResetPasswordPage />} />
      <Route path="/403" element={<ForbiddenPage />} />
      <Route path="/404" element={<NotFoundPage />} />

      <Route
        element={
          <AuthGuard>
            <AppLayout />
          </AuthGuard>
        }
      >
        <Route index element={<HomePage />} />
        <Route path="tin/:id" element={<ProductDetailPage />} />
        <Route path="tin/tao-moi" element={<AuthGuard roles={["ADMIN", "AGENT"]}><CreateListingPage /></AuthGuard>} />
        <Route path="tin/:id/chinh-sua" element={<AuthGuard roles={["ADMIN", "AGENT"]}><EditListingPage /></AuthGuard>} />
        <Route path="gio-hang-chung" element={<AuthGuard roles={["AGENT"]}><MyCartPage /></AuthGuard>} />
        <Route path="thong-bao" element={<NotificationsPage />} />
        <Route path="duyet/:queueType" element={<AuthGuard roles={["APPROVER", "ADMIN"]}><QueueListPage /></AuthGuard>} />
        <Route path="duyet/:queueType/:id" element={<AuthGuard roles={["APPROVER", "ADMIN"]}><QueueDetailPage /></AuthGuard>} />
        <Route path="nguoi-dung" element={<AuthGuard roles={["ADMIN"]}><UserListPage /></AuthGuard>} />
        <Route path="nguoi-dung/tao-moi" element={<AuthGuard roles={["ADMIN"]}><CreateUserPage /></AuthGuard>} />
        <Route path="nguoi-dung/:id/chinh-sua" element={<AuthGuard roles={["ADMIN"]}><EditUserPage /></AuthGuard>} />
        <Route path="tin-noi-bat" element={<AuthGuard roles={["ADMIN"]}><HotProductsPage /></AuthGuard>} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
          <Toaster />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
