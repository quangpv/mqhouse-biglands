import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import type { UseFormReturn } from "react-hook-form"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Label } from "@/shared/components/ui/label"
import type { IReportCancellationForm } from "../types"

interface CancellationDialogProps {
  open: boolean
  onClose: () => void
  onSubmit: (data: IReportCancellationForm) => void
  isPending: boolean
  form: UseFormReturn<IReportCancellationForm>
}

export function CancellationDialog({ open, onClose, onSubmit, isPending, form }: CancellationDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v) onClose() }}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Báo khách huỷ cọc</DialogTitle>
        </DialogHeader>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="cancel-reason">Lý do *</Label>
            <Input id="cancel-reason" {...form.register("notes")} placeholder="Nhập lý do huỷ cọc" />
            {form.formState.errors.notes && (
              <p className="text-xs text-destructive">{form.formState.errors.notes.message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Huỷ</Button>
            <Button type="submit" disabled={isPending}>
              {isPending ? "Đang xử lý..." : "Xác nhận"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
