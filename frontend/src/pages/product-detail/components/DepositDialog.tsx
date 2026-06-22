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

interface DepositDialogProps {
  open: boolean
  onClose: () => void
  onSubmit: (data: { customerName: string; customerPhone: string; depositAmount: number; notes: string }) => void
  isPending: boolean
}

export function DepositDialog({ open, onClose, onSubmit, isPending }: DepositDialogProps) {
  const [name, setName] = useState("")
  const [phone, setPhone] = useState("")
  const [amount, setAmount] = useState("")
  const [notes, setNotes] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = () => {
    const parsedAmount = Number(amount)
    if (!name.trim() || name.trim().length < 2) {
      setError("Vui lòng nhập tên khách hàng")
      return
    }
    if (!amount || isNaN(parsedAmount) || parsedAmount <= 0) {
      setError("Vui lòng nhập số tiền cọc hợp lệ")
      return
    }
    setError("")
    onSubmit({ customerName: name.trim(), customerPhone: phone.trim(), depositAmount: parsedAmount, notes: notes.trim() })
  }

  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v) { onClose(); setName(""); setPhone(""); setAmount(""); setNotes(""); setError("") }}}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Báo khách cọc</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="deposit-name">Tên khách hàng *</Label>
            <Input id="deposit-name" value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="deposit-phone">Số điện thoại</Label>
            <Input id="deposit-phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="deposit-amount">Số tiền cọc (VNĐ) *</Label>
            <Input id="deposit-amount" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="deposit-notes">Ghi chú</Label>
            <Input id="deposit-notes" value={notes} onChange={(e) => setNotes(e.target.value)} />
          </div>
          {error && <p className="text-xs text-destructive">{error}</p>}
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Huỷ</Button>
            <Button onClick={handleSubmit} disabled={isPending}>
              {isPending ? "Đang xử lý..." : "Xác nhận"}
            </Button>
          </DialogFooter>
        </div>
      </DialogContent>
    </Dialog>
  )
}
