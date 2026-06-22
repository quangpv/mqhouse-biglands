import { Card } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Badge } from "@/shared/components/ui/badge"
import { formatPrice } from "@/shared/utils"
import type { IHotProduct } from "../types"
import { Trash2, ChevronUp, ChevronDown, GripVertical } from "lucide-react"

interface HotProductItemProps {
  product: IHotProduct
  index: number
  total: number
  onMoveUp: () => void
  onMoveDown: () => void
  onRemove: () => void
}

export function HotProductItem({
  product,
  index,
  total,
  onMoveUp,
  onMoveDown,
  onRemove,
}: HotProductItemProps) {
  return (
    <Card className="flex items-center gap-3 p-3">
      <div className="flex flex-col gap-0.5 text-muted-foreground">
        <Button variant="ghost" size="icon" className="h-5 w-5" onClick={onMoveUp} disabled={index === 0}>
          <ChevronUp className="h-3 w-3" />
        </Button>
        <span className="text-center text-xs font-medium">{product.hotOrder}</span>
        <Button variant="ghost" size="icon" className="h-5 w-5" onClick={onMoveDown} disabled={index === total - 1}>
          <ChevronDown className="h-3 w-3" />
        </Button>
      </div>

      <div className="h-14 w-14 shrink-0 rounded-md overflow-hidden bg-muted">
        {product.primaryImageUrl ? (
          <img src={product.primaryImageUrl} alt="" className="h-full w-full object-cover" />
        ) : (
          <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
            No Image
          </div>
        )}
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{product.title}</p>
        <p className="text-xs text-muted-foreground">Mã tin: {product.productCode}</p>
        <p className="text-sm font-semibold text-primary">{formatPrice(product.price)}</p>
      </div>

      <Badge variant="default" className="bg-red-500 text-[10px]">Hot</Badge>

      <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0 text-destructive" onClick={onRemove}>
        <Trash2 className="h-4 w-4" />
      </Button>
    </Card>
  )
}
