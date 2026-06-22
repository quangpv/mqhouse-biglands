import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"

export function useUserListState() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState("")
  const [roleFilter, setRoleFilter] = useState<string>("")

  const query = useQuery({
    queryKey: userQueries.list({ page, search: search || undefined, role: roleFilter || undefined }),
    queryFn: () =>
      userRepository.list({ page, size: 20, search: search || undefined, role: roleFilter || undefined }),
  })

  const users = query.data?.data ?? []
  const totalPages = query.data?.pagination?.totalPages ?? 1

  return {
    users,
    totalPages,
    page,
    setPage,
    search,
    setSearch: (v: string) => { setSearch(v); setPage(1) },
    roleFilter,
    setRoleFilter: (v: string) => { setRoleFilter(v); setPage(1) },
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
    refetch: query.refetch,
  }
}
