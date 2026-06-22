export default function UserListPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Người dùng</h1>
      <p className="text-muted-foreground">User Management — List</p>
    </div>
  )
}

export function CreateUserPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Tạo người dùng</h1>
      <p className="text-muted-foreground">User Management — Create</p>
    </div>
  )
}

export function EditUserPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Chỉnh sửa người dùng</h1>
      <p className="text-muted-foreground">User Management — Edit</p>
    </div>
  )
}
