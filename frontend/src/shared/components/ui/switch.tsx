import * as React from "react"

import { cn } from "@/shared/utils/cn"

function Switch({ className, ...props }: React.ComponentProps<"button"> & { checked?: boolean; onCheckedChange?: (checked: boolean) => void }) {
  const [internalChecked, setInternalChecked] = React.useState(props.checked ?? false)
  const checked = props.checked ?? internalChecked

  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      data-state={checked ? "checked" : "unchecked"}
      data-slot="switch"
      className={cn(
        "peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border border-input shadow-xs transition-all outline-none",
        "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50",
        "disabled:pointer-events-none disabled:opacity-50",
        checked ? "bg-primary" : "bg-input",
        className
      )}
      onClick={() => {
        const next = !checked
        setInternalChecked(next)
        props.onCheckedChange?.(next)
      }}
      {...props}
    >
      <span
        data-slot="switch-thumb"
        className={cn(
          "pointer-events-none block h-4 w-4 rounded-full bg-background shadow-xs ring-0 transition-transform",
          checked ? "translate-x-4" : "translate-x-0.5"
        )}
      />
    </button>
  )
}

export { Switch }
