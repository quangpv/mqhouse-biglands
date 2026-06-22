import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import { Button } from "@/shared/components/ui/button"
import { Label } from "@/shared/components/ui/label"
import { Textarea } from "@/shared/components/ui/textarea"

interface ApproveConfirmDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onConfirm: (reason?: string) => void
  isPending: boolean
}

export function ApproveConfirmDialog({
  open,
  onOpenChange,
  onConfirm,
  isPending,
}: ApproveConfirmDialogProps) {
  const [reason, setReason] = useState("")

  const handleConfirm = () => {
    onConfirm(reason || undefined)
    setReason("")
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Xác nhận duyệt</DialogTitle>
          <DialogDescription>
            Bạn có chắc chắn muốn duyệt yêu cầu này?
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-2">
          <Label htmlFor="approve-reason">Ghi chú (không bắt buộc)</Label>
          <Textarea
            id="approve-reason"
            placeholder="Nhập ghi chú nếu cần..."
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Huỷ
          </Button>
          <Button onClick={handleConfirm} disabled={isPending}>
            {isPending ? "Đang duyệt..." : "Xác nhận duyệt"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
