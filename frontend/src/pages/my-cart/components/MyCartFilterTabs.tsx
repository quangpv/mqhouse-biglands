import type { MyCartTab } from "../types"

interface MyCartFilterTabsProps {
  tabs: Array<{ key: MyCartTab; label: string }>
  active: MyCartTab
  onTabChange: (tab: MyCartTab) => void
}

export function MyCartFilterTabs({ tabs, active, onTabChange }: MyCartFilterTabsProps) {
  return (
    <div className="flex flex-wrap gap-1 mb-4">
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
