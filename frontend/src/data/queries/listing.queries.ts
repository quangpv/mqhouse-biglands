export const listingQueries = {
  all: ["listings"] as const,
  lists: () => [...listingQueries.all, "list"] as const,
  list: (params: Record<string, unknown>) => [...listingQueries.lists(), params] as const,
  details: () => [...listingQueries.all, "detail"] as const,
  detail: (id: string) => [...listingQueries.details(), id] as const,
  pins: () => [...listingQueries.all, "pins"] as const,
}
