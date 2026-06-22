import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import type { MyCartTab } from "../types"

export function useMyCartState() {
  const [tab, setTab] = useState<MyCartTab>("all")
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)

  const statusFilter = tab === "all" ? undefined : [tab]

  const query = useQuery({
    queryKey: listingQueries.list({ tab: "my-cart", search, page, status: statusFilter }),
    queryFn: () =>
      listingRepository.list({
        createdBy: "me",
        status: statusFilter,
        q: search || undefined,
        page,
        size: 20,
      }),
  })

  const listings = query.data?.data ?? []

  const statusTabs: Array<{ key: MyCartTab; label: string }> = [
    { key: "all", label: "Tất cả" },
    { key: "DRAFT", label: "Nháp" },
    { key: "PENDING_APPROVAL", label: "Chờ duyệt" },
    { key: "CON_HANG", label: "Còn hàng" },
    { key: "DA_COC", label: "Đã cọc" },
    { key: "HET_HANG", label: "Hết hàng" },
    { key: "DA_CHOT", label: "Đã chốt" },
    { key: "HUY_COC", label: "Huỷ cọc" },
  ]

  return { query, listings, tab, setTab, search, setSearch, page, setPage, statusTabs }
}
