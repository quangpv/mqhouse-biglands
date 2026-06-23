import { useState, useMemo } from "react"
import { useQuery } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { dtoToIListing } from "@/shared/mappers/listing.mapper"
import type { IListing } from "@/shared/types/listing.type"
import type { IHotProduct } from "../types"

function toHotProduct(listing: IListing): IHotProduct {
  return {
    id: listing.id,
    listingId: listing.id,
    title: listing.title ?? listing.code ?? "",
    productCode: listing.code ?? "",
    primaryImageUrl: listing.primary_image_url ?? null,
    price: listing.price ?? 0,
    status: listing.status ?? "",
    hotOrder: listing.hot_order ?? 0,
  }
}

export function useHotProductsState() {
  const [orderMap, setOrderMap] = useState<Record<string, number>>({})

  const query = useQuery({
    queryKey: listingQueries.hot(),
    queryFn: () => listingRepository.getHotListings({ page: 1, size: 50 }),
  })

  const hotProducts = useMemo(() => {
    const items = (query.data?.data ?? []).map(dtoToIListing).map(toHotProduct)
    items.sort((a, b) => a.hotOrder - b.hotOrder)
    return items
  }, [query.data])

  const moveUp = (index: number) => {
    if (index <= 0) return
    const items = [...hotProducts]
    const temp = items[index].hotOrder
    items[index] = { ...items[index], hotOrder: items[index - 1].hotOrder }
    items[index - 1] = { ...items[index - 1], hotOrder: temp }
    items.sort((a, b) => a.hotOrder - b.hotOrder)
    const map: Record<string, number> = {}
    items.forEach((item, i) => {
      map[item.listingId] = i + 1
    })
    setOrderMap(map)
  }

  const moveDown = (index: number) => {
    if (index >= hotProducts.length - 1) return
    const items = [...hotProducts]
    const temp = items[index].hotOrder
    items[index] = { ...items[index], hotOrder: items[index + 1].hotOrder }
    items[index + 1] = { ...items[index + 1], hotOrder: temp }
    items.sort((a, b) => a.hotOrder - b.hotOrder)
    const map: Record<string, number> = {}
    items.forEach((item, i) => {
      map[item.listingId] = i + 1
    })
    setOrderMap(map)
  }

  const isReordered = Object.keys(orderMap).length > 0

  const getCurrentOrder = () => {
    if (isReordered) {
      return hotProducts.map((p) => ({
        listingId: p.listingId,
        hotOrder: orderMap[p.listingId] ?? p.hotOrder,
      }))
    }
    return hotProducts.map((p) => ({
      listingId: p.listingId,
      hotOrder: p.hotOrder,
    }))
  }

  const resetOrder = () => setOrderMap({})

  return {
    hotProducts,
    totalCount: query.data?.total ?? 0,
    orderMap,
    moveUp,
    moveDown,
    isReordered,
    getCurrentOrder,
    resetOrder,
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
    refetch: query.refetch,
  }
}
