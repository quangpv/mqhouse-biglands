export const userQueries = {
  all: ["users"] as const,
  lists: () => [...userQueries.all, "list"] as const,
  list: (params: Record<string, unknown>) => [...userQueries.lists(), params] as const,
  detail: (id: string) => [...userQueries.all, "detail", id] as const,
}
