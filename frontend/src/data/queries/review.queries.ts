export const reviewQueries = {
  all: ["reviews"] as const,
  list: (listingId: string) => [...reviewQueries.all, "list", listingId] as const,
}
