export interface IHotProduct {
  id: string
  listingId: string
  title: string
  productCode: string
  primaryImageUrl: string | null
  price: number
  status: string
  hotOrder: number
}

export interface ISearchableListing {
  id: string
  title: string
  productCode: string
  primaryImageUrl: string | null
  price: number
}
