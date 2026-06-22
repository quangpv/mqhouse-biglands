export function LoadingScreen() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full" />
    </div>
  )
}

export function LoadingSkeleton({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse bg-muted rounded-md ${className}`} />
}
