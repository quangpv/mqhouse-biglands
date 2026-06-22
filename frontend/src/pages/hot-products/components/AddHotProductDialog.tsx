import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/shared/components/ui/dialog"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { listingRepository } from "@/data/repositories/listing.repository"
import { formatPrice } from "@/shared/utils"
import { Search } from "lucide-react"

interface AddHotProductDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSelect: (listingId: string) => void
  currentCount: number
}

export function AddHotProductDialog({
  open,
  onOpenChange,
  onSelect,
  currentCount,
}: AddHotProductDialogProps) {
  const [search, setSearch] = useState("")

  const query = useQuery({
    queryKey: ["listings", "non-hot", search],
    queryFn: () => listingRepository.list({ isHot: false, q: search || undefined, page: 1, size: 20 }),
    enabled: open,
  })

  const listings = query.data?.data ?? []
  const atMax = currentCount >= 14

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Thêm tin nổi bật</DialogTitle>
          <DialogDescription>
            {atMax
              ? "Đã đạt số lượng tối đa 14 tin."
              : "Tìm kiếm tin đăng để thêm vào danh sách nổi bật."}
          </DialogDescription>
        </DialogHeader>

        {!atMax && (
          <>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Tìm kiếm theo mã tin, địa chỉ..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>

            <div className="max-h-60 space-y-1 overflow-y-auto">
              {listings.length === 0 ? (
                <p className="text-center text-sm text-muted-foreground py-4">
                  {query.isLoading ? "Đang tải..." : "Không tìm thấy tin nào"}
                </p>
              ) : (
                listings.map((listing) => (
                  <button
                    key={listing.id}
                    type="button"
                    className="flex w-full items-center gap-3 rounded-md p-2 text-left text-sm hover:bg-accent"
                    onClick={() => {
                      onSelect(listing.id)
                      onOpenChange(false)
                      setSearch("")
                    }}
                  >
                    <div className="h-10 w-10 shrink-0 rounded bg-muted overflow-hidden">
                      {listing.primaryImageUrl && (
                        <img src={listing.primaryImageUrl} alt="" className="h-full w-full object-cover" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="truncate font-medium">{listing.title || listing.productCode}</p>
                      <p className="text-xs text-muted-foreground">{formatPrice(listing.price)}</p>
                    </div>
                  </button>
                ))
              )}
            </div>
          </>
        )}

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Đóng
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
