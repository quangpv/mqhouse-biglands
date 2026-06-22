import type { NotificationFilter } from "../types"

interface NotificationFilterTabsProps {
  tabs: Array<{ key: NotificationFilter; label: string }>
  active: NotificationFilter
  onTabChange: (tab: NotificationFilter) => void
}

export function NotificationFilterTabs({ tabs, active, onTabChange }: NotificationFilterTabsProps) {
  return (
    <div className="flex gap-1 mb-4">
      {tabs.map((t) => (
        <button
          key={t.key}
          onClick={() => onTabChange(t.key)}
          className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
            active === t.key
              ? "bg-primary text-primary-foreground font-medium"
              : "bg-muted text-muted-foreground hover:bg-accent"
          }`}
        >
          {t.label}
        </button>
      ))}
    </div>
  )
}
