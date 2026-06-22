import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import { Button } from "@/shared/components/ui/button"

interface DeactivateConfirmDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onConfirm: () => void
  isPending: boolean
  userName: string
  isCurrentlyActive: boolean
}

export function DeactivateConfirmDialog({
  open,
  onOpenChange,
  onConfirm,
  isPending,
  userName,
  isCurrentlyActive,
}: DeactivateConfirmDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{isCurrentlyActive ? "Vô hiệu hoá người dùng" : "Kích hoạt người dùng"}</DialogTitle>
          <DialogDescription>
            {isCurrentlyActive
              ? `Người dùng "${userName}" sẽ không thể đăng nhập vào hệ thống.`
              : `Kích hoạt lại quyền truy cập cho "${userName}".`}
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Huỷ
          </Button>
          <Button
            variant={isCurrentlyActive ? "destructive" : "default"}
            onClick={onConfirm}
            disabled={isPending}
          >
            {isPending
              ? "Đang xử lý..."
              : isCurrentlyActive
                ? "Xác nhận vô hiệu hoá"
                : "Xác nhận kích hoạt"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
