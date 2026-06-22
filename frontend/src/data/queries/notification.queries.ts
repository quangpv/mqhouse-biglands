export const notificationQueries = {
  all: ["notifications"] as const,
  lists: () => [...notificationQueries.all, "list"] as const,
  list: (params: Record<string, unknown>) => [...notificationQueries.lists(), params] as const,
  unreadCount: () => [...notificationQueries.all, "unread-count"] as const,
  preferences: () => [...notificationQueries.all, "preferences"] as const,
}
