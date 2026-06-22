import { useNotificationState } from "./facades/useNotificationState"
import { useMarkRead } from "./facades/useMarkRead"
import { useMarkAllRead } from "./facades/useMarkAllRead"
import { useNotificationPreferences } from "./facades/useNotificationPreferences"
import { useNotificationMapper } from "./hooks/useNotificationMapper"
import { NotificationFilterTabs } from "./components/NotificationFilterTabs"
import { NotificationItem } from "./components/NotificationItem"
import { PageHeader } from "@/shared/components/page-header"
import { Button } from "@/shared/components/ui/button"
import { LoadingSkeleton } from "@/shared/components/loading-screen"
import { EmptyState } from "@/shared/components/empty-state"
import { ErrorDisplay } from "@/shared/components/error-display"
import { Settings, Bell } from "lucide-react"
import { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle } from "@/shared/components/ui/sheet"
import { Switch } from "@/shared/components/ui/switch"
import { Label } from "@/shared/components/ui/label"

const preferenceLabels: Record<string, string> = {
  listingPostCreated: "Có tin đăng mới chờ duyệt",
  listingPostApproved: "Tin đăng được duyệt",
  listingPostRejected: "Tin đăng bị từ chối",
  depositReported: "Có báo cọc mới",
  depositConfirmed: "Cọc được xác nhận",
  depositRejected: "Cọc bị từ chối",
  closureReported: "Có báo tất toán mới",
  closureConfirmed: "Tất toán được xác nhận",
  closureRejected: "Tất toán bị từ chối",
  cancellationReported: "Có báo huỷ cọc mới",
  cancellationConfirmed: "Huỷ cọc được xác nhận",
  cancellationRejected: "Huỷ cọc bị từ chối",
  soldOutReported: "Có báo hết hàng mới",
  soldOutConfirmed: "Hết hàng được xác nhận",
  listingExpired: "Tin đăng hết hạn",
}

export default function NotificationsPage() {
  const { listQuery, unreadCount, notifications, filter, setFilter, filterTabs } =
    useNotificationState()
  const { mutate: markRead } = useMarkRead()
  const { mutate: doMarkAllRead, isPending: isMarkingAll } = useMarkAllRead()
  const { query: prefsQuery, updateMutation } = useNotificationPreferences()
  const { toUI } = useNotificationMapper()

  return (
    <div>
      <PageHeader
        title="Thông báo"
        description={unreadCount > 0 ? `${unreadCount} thông báo chưa đọc` : undefined}
        action={
          <div className="flex items-center gap-2">
            {unreadCount > 0 && (
              <Button variant="outline" size="sm" onClick={() => doMarkAllRead()} disabled={isMarkingAll}>
                Đánh dấu đã đọc
              </Button>
            )}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon">
                  <Settings className="h-4 w-4" />
                </Button>
              </SheetTrigger>
              <SheetContent>
                <SheetHeader>
                  <SheetTitle>Cài đặt thông báo</SheetTitle>
                </SheetHeader>
                <div className="space-y-4 mt-6">
                  {prefsQuery.isLoading ? (
                    <LoadingSkeleton className="h-40 w-full" />
                  ) : prefsQuery.data ? (
                    Object.entries(preferenceLabels).map(([key, label]) => (
                      <div key={key} className="flex items-center justify-between">
                        <Label htmlFor={key} className="text-sm cursor-pointer">{label}</Label>
                        <Switch
                          id={key}
                          checked={(prefsQuery.data as Record<string, boolean>)[key] ?? true}
                          onCheckedChange={(checked) =>
                            updateMutation.mutate({ [key]: checked })
                          }
                        />
                      </div>
                    ))
                  ) : null}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        }
      />

      <NotificationFilterTabs tabs={filterTabs} active={filter} onTabChange={setFilter} />

      <div className="space-y-2">
        {listQuery.isLoading ? (
          Array.from({ length: 8 }).map((_, i) => (
            <LoadingSkeleton key={i} className="h-20 w-full" />
          ))
        ) : listQuery.isError ? (
          <ErrorDisplay message="Không thể tải thông báo" onRetry={() => listQuery.refetch()} />
        ) : notifications.length === 0 ? (
          <EmptyState
            message="Không có thông báo"
            description={filter === "unread" ? "Bạn đã đọc tất cả thông báo" : "Chưa có thông báo nào"}
          />
        ) : (
          notifications.map((n) => (
            <NotificationItem key={n.id} notification={toUI(n)} onMarkRead={markRead} />
          ))
        )}
      </div>
    </div>
  )
}
