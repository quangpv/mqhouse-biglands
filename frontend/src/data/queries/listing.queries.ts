export const listingQueries = {
  all: ["listings"] as const,
  lists: () => [...listingQueries.all, "list"] as const,
  list: (params: Record<string, unknown>) => [...listingQueries.lists(), params] as const,
  hot: () => [...listingQueries.all, "hot"] as const,
  hotStrip: () => [...listingQueries.all, "hot-strip"] as const,
  pins: () => [...listingQueries.all, "pins"] as const,
  filterCounts: () => [...listingQueries.all, "filter-counts"] as const,
  details: () => [...listingQueries.all, "detail"] as const,
  detail: (id: string) => [...listingQueries.details(), id] as const,
}
