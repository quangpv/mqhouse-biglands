import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Label } from "@/shared/components/ui/label"

interface ClosureDialogProps {
  open: boolean
  onClose: () => void
  onSubmit: (notes: string) => void
  isPending: boolean
}

export function ClosureDialog({ open, onClose, onSubmit, isPending }: ClosureDialogProps) {
  const [notes, setNotes] = useState("")

  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v) { onClose(); setNotes("") }}}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Báo khách chốt hàng</DialogTitle>
        </DialogHeader>
        <div className="space-y-2">
          <Label htmlFor="closure-notes">Ghi chú</Label>
          <Input id="closure-notes" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Ghi chú (không bắt buộc)" />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Huỷ</Button>
          <Button onClick={() => onSubmit(notes)} disabled={isPending}>
            {isPending ? "Đang xử lý..." : "Xác nhận"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
