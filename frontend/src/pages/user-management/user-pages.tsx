import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { userRepository } from "@/data/repositories/user.repository"
import { userQueries } from "@/data/queries/user.queries"
import { PageHeader } from "@/shared/components/page-header"
import { Input } from "@/shared/components/ui/input"
import { Button } from "@/shared/components/ui/button"
import { Select } from "@/shared/components/ui/select"
import { EmptyState } from "@/shared/components/empty-state"
import { UserTable } from "./components/UserTable"
import { UserForm } from "./components/UserForm"
import { DeactivateConfirmDialog } from "./components/UserActionDialogs"
import { useUserListState } from "./facades/useUserListState"
import { useCreateUser } from "./facades/useCreateUser"
import { useUpdateUser } from "./facades/useUpdateUser"
import { useDeactivateUser } from "./facades/useDeactivateUser"
import { useUserFormState } from "./facades/useUserFormState"
import { toUserTableRow } from "./hooks/useUserMapper"
import { Plus, Search } from "lucide-react"

export default function UserListPage() {
  const navigate = useNavigate()
  const { search, setSearch, roleFilter, setRoleFilter, users, totalPages, page, setPage, isLoading, isError, refetch } = useUserListState()
  const deactivateUser = useDeactivateUser()
  const [deactivateTarget, setDeactivateTarget] = useState<{ id: string; name: string; isActive: boolean } | null>(null)

  const mappedUsers = users.map(toUserTableRow)

  return (
    <div>
      <PageHeader
        title="Quản lý người dùng"
        action={
          <Button onClick={() => navigate("/nguoi-dung/tao-moi")}>
            <Plus className="h-4 w-4 mr-1" />
            Tạo người dùng
          </Button>
        }
      />

      <div className="mb-4 flex items-center gap-3">
        <div className="relative max-w-sm flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Tìm kiếm theo tên, tài khoản, số điện thoại..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select
          value={roleFilter}
          onValueChange={setRoleFilter}
          placeholder="Tất cả vai trò"
          options={[
            { value: "AGENT", label: "Môi giới" },
            { value: "APPROVER", label: "Người duyệt" },
            { value: "ADMIN", label: "Quản trị viên" },
          ]}
        />
      </div>

      {isError ? (
        <EmptyState message="Không thể tải danh sách" actionLabel="Thử lại" onAction={refetch} />
      ) : (
        <UserTable
          users={mappedUsers}
          totalPages={totalPages}
          page={page}
          setPage={setPage}
          isLoading={isLoading}
          onEdit={(id) => navigate(`/nguoi-dung/${id}/chinh-sua`)}
          onToggleActive={(id, currentActive) => {
            const user = users.find((u) => u.id === id)
            if (user) setDeactivateTarget({ id, name: user.fullName, isActive: currentActive })
          }}
          onChangeRole={(id) => {}}
        />
      )}

      <DeactivateConfirmDialog
        open={!!deactivateTarget}
        onOpenChange={(open) => { if (!open) setDeactivateTarget(null) }}
        onConfirm={() => {
          if (deactivateTarget) {
            deactivateUser.mutate({ id: deactivateTarget.id, isActive: deactivateTarget.isActive })
            setDeactivateTarget(null)
          }
        }}
        isPending={deactivateUser.isPending}
        userName={deactivateTarget?.name ?? ""}
        isCurrentlyActive={deactivateTarget?.isActive ?? false}
      />
    </div>
  )
}

export function CreateUserPage() {
  const { form } = useUserFormState(null)
  const { mutate: create, isPending } = useCreateUser()

  return (
    <div>
      <PageHeader title="Tạo người dùng" backPath="/nguoi-dung" />
      <UserForm form={form} mode="create" onSubmit={(data) => create(data)} isPending={isPending} />
    </div>
  )
}

export function EditUserPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const userQuery = useQuery({
    queryKey: userQueries.detail(id ?? ""),
    queryFn: () => userRepository.get(id ?? ""),
    enabled: !!id,
  })

  const { form } = useUserFormState(userQuery.data ?? null)
  const { mutate: update, isPending } = useUpdateUser(id ?? "")

  if (userQuery.isLoading) return <PageHeader title="Đang tải..." backPath="/nguoi-dung" />
  if (userQuery.isError) {
    return (
      <div>
        <PageHeader title="Có lỗi xảy ra" backPath="/nguoi-dung" />
        <p className="text-muted-foreground">Không thể tải thông tin người dùng</p>
      </div>
    )
  }

  return (
    <div>
      <PageHeader title="Chỉnh sửa người dùng" backPath="/nguoi-dung" />
      <UserForm form={form} mode="edit" onSubmit={(data) => update(data)} isPending={isPending} />
    </div>
  )
}
