export function ForbiddenPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className="text-4xl font-bold">403</h1>
      <p className="text-muted-foreground">Bạn không có quyền truy cập trang này</p>
      <a href="/" className="text-sm text-primary underline">Về trang chủ</a>
    </div>
  )
}

export function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className="text-4xl font-bold">404</h1>
      <p className="text-muted-foreground">Trang không tìm thấy</p>
      <a href="/" className="text-sm text-primary underline">Về trang chủ</a>
    </div>
  )
}
