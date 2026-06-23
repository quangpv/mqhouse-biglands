import { useState } from "react"
import { Outlet, Link, useNavigate, useLocation } from "react-router-dom"
import { Bell } from "lucide-react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { useAuthStore } from "@/shared/context/auth-store"
import { useNotificationWebSocket } from "@/shared/hooks/useNotificationWebSocket"
import { Button } from "@/shared/components/ui/button"
import { Badge } from "@/shared/components/ui/badge"
import { Sheet, SheetTrigger, SheetContent } from "@/shared/components/ui/sheet"
import { notificationQueries } from "@/data/queries/notification.queries"
import { notificationRepository } from "@/data/repositories/notification.repository"

const navItems = [
  { path: "/", label: "Trang chủ", roles: ["AGENT", "APPROVER", "ADMIN"] },
  { path: "/gio-hang-chung", label: "Giỏ hàng của tôi", roles: ["AGENT", "APPROVER", "ADMIN"] },
  { path: "/thong-bao", label: "Thông báo", roles: ["AGENT", "APPROVER", "ADMIN"] },
  { path: "/duyet/listing-post", label: "Duyệt tin", roles: ["APPROVER", "ADMIN"] },
  { path: "/nguoi-dung", label: "Người dùng", roles: ["ADMIN"] },
  { path: "/tin-noi-bat", label: "Tin nổi bật", roles: ["ADMIN"] },
]

export function AppLayout() {
  const { user, clearAuth } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const queryClient = useQueryClient()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useNotificationWebSocket()

  const unreadQuery = useQuery({
    queryKey: notificationQueries.unreadCount(),
    queryFn: () => notificationRepository.getUnreadCount(),
    enabled: !!user,
    refetchInterval: 60_000,
  })
  const unreadCount = unreadQuery.data?.count ?? 0

  const handleLogout = () => {
    clearAuth()
    navigate("/dang-nhap")
  }

  const canShow = (roles: string[]) => user && roles.includes(user.role)

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center gap-4 px-4 lg:px-6">
          <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="lg:hidden">
                <span className="sr-only">Menu</span>
                <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 6h16M4 12h16M4 18h16" /></svg>
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-64">
              <nav className="flex flex-col gap-2 pt-6">
                {navItems.filter((i) => canShow(i.roles)).map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setSidebarOpen(false)}
                    className={`px-3 py-2 rounded-md text-sm ${location.pathname === item.path ? "bg-accent font-medium" : "hover:bg-accent"}`}
                  >
                    {item.label}
                  </Link>
                ))}
              </nav>
            </SheetContent>
          </Sheet>

          <Link to="/" className="font-semibold text-lg">Biglands</Link>

          <nav className="hidden lg:flex items-center gap-1 ml-6">
            {navItems.filter((i) => canShow(i.roles)).map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-md text-sm ${location.pathname === item.path ? "bg-accent font-medium" : "hover:bg-accent"}`}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-2">
            <Button variant="ghost" size="icon" className="relative" onClick={() => navigate("/thong-bao")}>
              <Bell className="h-5 w-5" />
              {unreadCount > 0 && (
                <Badge className="absolute -top-1 -right-1 h-4 min-w-4 px-1 text-[10px] flex items-center justify-center">
                  {unreadCount > 99 ? "99+" : unreadCount}
                </Badge>
              )}
            </Button>
            <span className="text-sm text-muted-foreground hidden sm:inline">{user?.fullName}</span>
            <Button variant="outline" size="sm" onClick={handleLogout}>Đăng xuất</Button>
          </div>
        </div>
      </header>

      <main className="flex-1 p-4 lg:p-6">
        <Outlet />
      </main>
    </div>
  )
}
