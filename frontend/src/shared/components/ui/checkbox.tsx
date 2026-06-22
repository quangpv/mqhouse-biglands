import * as React from "react"

import { cn } from "@/shared/utils/cn"

function Checkbox({ className, checked, onCheckedChange, ...props }: React.ComponentProps<"button"> & { checked?: boolean; onCheckedChange?: (checked: boolean) => void }) {
  const [internalChecked, setInternalChecked] = React.useState(checked ?? false)
  const isChecked = checked ?? internalChecked

  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={isChecked}
      data-state={isChecked ? "checked" : "unchecked"}
      data-slot="checkbox"
      className={cn(
        "peer h-4 w-4 shrink-0 rounded-sm border border-input shadow-xs outline-none transition-all",
        "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50",
        "disabled:pointer-events-none disabled:opacity-50",
        isChecked ? "bg-primary border-primary text-primary-foreground" : "bg-transparent",
        className
      )}
      onClick={() => {
        const next = !isChecked
        setInternalChecked(next)
        onCheckedChange?.(next)
      }}
      {...props}
    >
      {isChecked && (
        <svg viewBox="0 0 16 16" fill="none" className="h-full w-full stroke-current">
          <path d="M3 8L6.5 11.5L13 5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </button>
  )
}

export { Checkbox }
