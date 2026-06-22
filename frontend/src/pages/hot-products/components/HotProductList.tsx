import { HotProductItem } from "./HotProductItem"
import type { IHotProduct } from "../types"

interface HotProductListProps {
  products: IHotProduct[]
  onMoveUp: (index: number) => void
  onMoveDown: (index: number) => void
  onRemove: (listingId: string) => void
}

export function HotProductList({ products, onMoveUp, onMoveDown, onRemove }: HotProductListProps) {
  return (
    <div className="space-y-2">
      {products.map((product, index) => (
        <HotProductItem
          key={product.listingId}
          product={product}
          index={index}
          total={products.length}
          onMoveUp={() => onMoveUp(index)}
          onMoveDown={() => onMoveDown(index)}
          onRemove={() => onRemove(product.listingId)}
        />
      ))}
    </div>
  )
}
