import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import { Button } from "@/shared/components/ui/button"
import { getStatusLabel } from "@/shared/utils"

interface BlockedActionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  status: string
  actionLabel: string
}

export function BlockedActionDialog({
  open,
  onOpenChange,
  status,
  actionLabel,
}: BlockedActionDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Không thể thực hiện thao tác</DialogTitle>
          <DialogDescription>
            Tin đã ở trạng thái <strong>{getStatusLabel(status)}</strong>, không thể{" "}
            {actionLabel}.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button onClick={() => onOpenChange(false)}>Đã hiểu</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
