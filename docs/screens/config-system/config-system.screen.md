# Config System Screen

## Overview

Admin-only configuration screen for managing system entities. Uses a tabbed interface with 4 tabs: Tổ chức (Organizations), Loại giao dịch (Transaction Types), Loại bất động sản (Property Types), Nhãn (Tags).

### Route
`/cau-hinh-he-thong`

### Role Guard
`ADMIN` only

### Page Layout
- `PageHeader` with title "Cấu hình hệ thống"
- Tabs component (`Tabs` from shadcn/ui) with 4 tab triggers:
  - "Tổ chức" (default, index 0)
  - "Loại giao dịch"
  - "Loại bất động sản"
  - "Nhãn"
- Each tab contains a data table with entity-specific columns and action buttons
- Create/Edit operations open modal `Dialog` components
- Delete operations open confirmation `Dialog`

---

# Tab 1 — Quản lý tổ chức (Organizations)

## APIs

### GET /api/v1/organizations/

List Endpoint — returns all organizations.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| No parameters | | | |

**Response (200)**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "org_biglands",
    "display_name": "Biglands Corp",
    "transaction_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    "property_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    "created_at": "2026-06-25T10:00:00"
  }
]
```

### POST /api/v1/organizations/

Create Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | unique, system identifier |
| `display_name` | string | yes | UI display name |
| `transaction_types` | uuid[] | yes | references TransactionType IDs |
| `property_types` | uuid[] | yes | references PropertyType IDs |

**Request**
```json
{
  "name": "org_biglands",
  "display_name": "Biglands Corp",
  "transaction_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
  "property_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
}
```

**Response (201)**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "org_biglands",
  "display_name": "Biglands Corp",
  "transaction_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
  "property_types": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
  "created_at": "2026-06-25T10:00:00"
}
```

### PUT /api/v1/organizations/{org_id}

Update Endpoint.

**Path Parameter:** `org_id` (uuid)

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | unique, system identifier |
| `display_name` | string | yes | UI display name |
| `transaction_types` | uuid[] | yes | references TransactionType IDs |
| `property_types` | uuid[] | yes | references PropertyType IDs |

**Response (200)** — Same as Create response.

### DELETE /api/v1/organizations/{org_id}

Delete Endpoint.

**Path Parameter:** `org_id` (uuid)

**Response (204)** — No content. Returns `null`.

### Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## Screen States — Organizations Tab

### Idle
- DataTable with columns:
  | # | Tên tổ chức | Tên hiển thị | Loại giao dịch | Loại BĐS | Ngày tạo | Thao tác |
  |---|-------------|--------------|----------------|----------|----------|----------|
- Each entity row shows `name`, `display_name`, comma-separated list of transaction/property type display names, `created_at` formatted as date
- Actions column: Edit (Pencil icon button), Delete (Trash2 icon button)
- PageHeader action slot: "Thêm tổ chức" Button (Plus icon)
- Pagination at bottom if > 1 page (page numbers + prev/next)

### Loading
- Table skeleton: 5 rows of shimmer placeholders
- Action buttons disabled

### Empty
- `<EmptyState>` component
- Icon: Building2
- Message: "Chưa có tổ chức nào"
- Action: "Thêm tổ chức" button

### Dialog — Create Organization
- Modal dialog with title "Thêm tổ chức mới"
- Form fields inside Card:
  - `name` (Input) — text, placeholder "Tên tổ chức (hệ thống)"
  - `display_name` (Input) — text, placeholder "Tên hiển thị"
  - `transaction_types` (Multi-select Command + Badge) — searchable dropdown with checkboxes listing all transaction types
  - `property_types` (Multi-select Command + Badge) — searchable dropdown with checkboxes listing all property types
- Submit button: "Tạo tổ chức" (disabled while submitting, shows spinner + "Đang tạo...")
- Cancel button: "Hủy"
- All multi-select dropdowns fetch `TransactionTypeResponse[]` and `PropertyTypeResponse[]` lists independently for options

### Dialog — Edit Organization
- Title: "Chỉnh sửa tổ chức"
- Same form layout as Create, pre-filled with existing values
- Submit button: "Lưu thay đổi" (disabled while submitting, shows spinner + "Đang lưu...")
- Cancel button: "Hủy"

### Dialog — Delete Confirmation
- Title: "Xóa tổ chức"
- Message: "Bạn có chắc chắn muốn xóa tổ chức **[display_name]**? Hành động này không thể hoàn tác."
- Two buttons:
  - "Hủy" (outline variant)
  - "Xóa" (destructive variant, disabled while submitting, shows spinner + "Đang xóa...")

### Error — Validation (422)
- Dialog stays open
- Field-level errors shown below each invalid field (red text)
- Top error banner in dialog: "Vui lòng kiểm tra lại thông tin"

### Error — Network / Server Error
- Toast notification: "Không thể kết nối đến máy chủ. Vui lòng thử lại."
- Dialog stays open, fields remain editable

### Error — Conflict (Delete blocked)
- Toast: "Không thể xóa tổ chức này vì đang có người dùng tham chiếu"
- Dialog closes, nothing changes in table

---

# Tab 2 — Quản lý loại giao dịch (Transaction Types)

## APIs

### GET /api/v1/transaction-types/

List Endpoint.

**Response (200)**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "code": "sell",
    "display_name": "Bán",
    "created_at": "2026-06-25T10:00:00",
    "updated_at": "2026-06-25T10:00:00"
  }
]
```

### POST /api/v1/transaction-types/

Create Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `code` | string | yes | unique, lowercase system code |
| `display_name` | string | yes | UI display name |

**Request**
```json
{
  "code": "sell",
  "display_name": "Bán"
}
```

**Response (201)**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "code": "sell",
  "display_name": "Bán",
  "created_at": "2026-06-25T10:00:00",
  "updated_at": "2026-06-25T10:00:00"
}
```

### GET /api/v1/transaction-types/{entity_id}

Get Endpoint.

### PUT /api/v1/transaction-types/{entity_id}

Update Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `code` | string | yes | unique, lowercase system code |
| `display_name` | string | yes | UI display name |

**Response (200)** — Same `TransactionTypeResponse`.

### DELETE /api/v1/transaction-types/{entity_id}

Delete Endpoint.

**Response (204)** — No content.

---

## Screen States — Transaction Types Tab

### Idle
- DataTable with columns:
  | # | Mã (code) | Tên hiển thị | Ngày tạo | Thao tác |
  |---|-----------|---------------|----------|----------|
- Actions: Edit (Pencil), Delete (Trash2)
- Header action: "Thêm loại giao dịch" Button (Plus icon)
- Pagination at bottom if > 1 page

### Loading
- Table skeleton: 5 rows of shimmer placeholders

### Empty
- `<EmptyState>` with icon `ArrowLeftRight`
- Message: "Chưa có loại giao dịch nào"
- Action: "Thêm loại giao dịch" button

### Dialog — Create Transaction Type
- Title: "Thêm loại giao dịch mới"
- Fields:
  - `code` (Input) — text, placeholder "Ví dụ: sell, rent"
  - `display_name` (Input) — text, placeholder "Tên hiển thị, ví dụ: Bán, Cho thuê"
- Submit: "Tạo loại giao dịch" / "Đang tạo..."
- Cancel: "Hủy"

### Dialog — Edit Transaction Type
- Title: "Chỉnh sửa loại giao dịch"
- Same form, pre-filled
- Submit: "Lưu thay đổi" / "Đang lưu..."

### Dialog — Delete Confirmation
- Title: "Xóa loại giao dịch"
- Message: "Bạn có chắc chắn muốn xóa loại giao dịch **[display_name]**? Hành động này không thể hoàn tác."
- Two buttons: "Hủy", "Xóa" (destructive)

### Error — Validation (422)
- Field-level inline errors
- Top banner: "Vui lòng kiểm tra lại thông tin"

### Error — Network / Server Error
- Toast: "Không thể kết nối đến máy chủ. Vui lòng thử lại."

### Error — Conflict (Delete blocked by Organization reference)
- Toast: "Không thể xóa loại giao dịch này vì đang được tổ chức sử dụng"
- Dialog closes

---

# Tab 3 — Quản lý loại bất động sản (Property Types)

## APIs

### GET /api/v1/property-types/

List Endpoint.

**Response (200)**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "code": "apartment",
    "display_name": "Căn hộ",
    "created_at": "2026-06-25T10:00:00",
    "updated_at": "2026-06-25T10:00:00"
  }
]
```

### POST /api/v1/property-types/

Create Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `code` | string | yes | unique, lowercase system code |
| `display_name` | string | yes | UI display name |

**Request**
```json
{
  "code": "apartment",
  "display_name": "Căn hộ"
}
```

**Response (201)**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "code": "apartment",
  "display_name": "Căn hộ",
  "created_at": "2026-06-25T10:00:00",
  "updated_at": "2026-06-25T10:00:00"
}
```

### GET /api/v1/property-types/{entity_id}

Get Endpoint.

### PUT /api/v1/property-types/{entity_id}

Update Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `code` | string | yes | unique, lowercase system code |
| `display_name` | string | yes | UI display name |

**Response (200)** — Same `PropertyTypeResponse`.

### DELETE /api/v1/property-types/{entity_id}

Delete Endpoint.

**Response (204)** — No content.

---

## Screen States — Property Types Tab

### Idle
- DataTable with columns:
  | # | Mã (code) | Tên hiển thị | Ngày tạo | Thao tác |
  |---|-----------|---------------|----------|----------|
- Actions: Edit (Pencil), Delete (Trash2)
- Header action: "Thêm loại bất động sản" Button (Plus icon)
- Pagination at bottom if > 1 page

### Loading
- Table skeleton: 5 rows of shimmer placeholders

### Empty
- `<EmptyState>` with icon `Home`
- Message: "Chưa có loại bất động sản nào"
- Action: "Thêm loại bất động sản" button

### Dialog — Create Property Type
- Title: "Thêm loại bất động sản mới"
- Fields:
  - `code` (Input) — text, placeholder "Ví dụ: apartment, house"
  - `display_name` (Input) — text, placeholder "Tên hiển thị, ví dụ: Căn hộ, Nhà phố"
- Submit: "Tạo loại bất động sản" / "Đang tạo..."
- Cancel: "Hủy"

### Dialog — Edit Property Type
- Title: "Chỉnh sửa loại bất động sản"
- Same form, pre-filled
- Submit: "Lưu thay đổi" / "Đang lưu..."

### Dialog — Delete Confirmation
- Title: "Xóa loại bất động sản"
- Message: "Bạn có chắc chắn muốn xóa loại bất động sản **[display_name]**? Hành động này không thể hoàn tác."
- Two buttons: "Hủy", "Xóa" (destructive)

### Error — Validation (422)
- Field-level inline errors
- Top banner: "Vui lòng kiểm tra lại thông tin"

### Error — Network / Server Error
- Toast: "Không thể kết nối đến máy chủ. Vui lòng thử lại."

### Error — Conflict (Delete blocked by Organization reference)
- Toast: "Không thể xóa loại bất động sản này vì đang được tổ chức sử dụng"
- Dialog closes

---

# Tab 4 — Quản lý nhãn (Tags)

## APIs

### GET /api/v1/tags/

List Endpoint.

**Response (200)**
```json
[
  {
    "id": "trung-tam",
    "display_name": "Trung tâm",
    "created_at": "2026-06-25T10:00:00",
    "updated_at": "2026-06-25T10:00:00"
  }
]
```

### POST /api/v1/tags/

Create Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `id` | string | no | custom slug; auto-generated from display_name if null |
| `display_name` | string | yes | UI display name |

**Request**
```json
{
  "id": null,
  "display_name": "Trung tâm"
}
```

**Response (201)**
```json
{
  "id": "trung-tam",
  "display_name": "Trung tâm",
  "created_at": "2026-06-25T10:00:00",
  "updated_at": "2026-06-25T10:00:00"
}
```

### GET /api/v1/tags/{tag_id}

Get Endpoint.

### PUT /api/v1/tags/{tag_id}

Update Endpoint.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `display_name` | string | yes | UI display name (id/slug is immutable) |

**Response (200)** — Same `TagResponse`.

### DELETE /api/v1/tags/{tag_id}

Delete Endpoint.

**Response (204)** — No content.

---

## Screen States — Tags Tab

### Idle
- DataTable with columns:
  | Slug (id) | Tên hiển thị | Ngày tạo | Thao tác |
  |-----------|---------------|----------|----------|
- Actions: Edit (Pencil), Delete (Trash2)
- Header action: "Thêm nhãn" Button (Plus icon)
- Pagination at bottom if > 1 page

### Loading
- Table skeleton: 5 rows of shimmer placeholders

### Empty
- `<EmptyState>` with icon `Tag`
- Message: "Chưa có nhãn nào"
- Action: "Thêm nhãn" button

### Dialog — Create Tag
- Title: "Thêm nhãn mới"
- Fields:
  - `display_name` (Input) — text, placeholder "Nhập tên nhãn, ví dụ: Trung tâm"
  - `slug` (Input) — text, placeholder "Để trống để tự động tạo từ tên nhãn, ví dụ: trung-tam" (optional)
- Slug auto-filled if left empty: lowercase, replace spaces with hyphens, remove accents
- Submit: "Tạo nhãn" / "Đang tạo..."
- Cancel: "Hủy"

### Dialog — Edit Tag
- Title: "Chỉnh sửa nhãn"
- Same form, pre-filled (slug field read-only/disabled)
- Submit: "Lưu thay đổi" / "Đang lưu..."

### Dialog — Delete Confirmation
- Title: "Xóa nhãn"
- Message: "Bạn có chắc chắn muốn xóa nhãn **[display_name]**? Hành động này không thể hoàn tác."
- Two buttons: "Hủy", "Xóa" (destructive)

### Error — Validation (422)
- Field-level inline errors
- Top banner: "Vui lòng kiểm tra lại thông tin"

### Error — Network / Server Error
- Toast: "Không thể kết nối đến máy chủ. Vui lòng thử lại."

### Error — Conflict (Delete blocked by Property reference)
- Toast: "Không thể xóa nhãn này vì đang được bất động sản sử dụng"
- Dialog closes

---

# Shared Behaviors

### Tab Switching
- Active tab is tracked in local state (useState with index or string key)
- Data for each tab is fetched independently via separate TanStack Query hooks
- Switching tabs is instant (data cached after first load)
- No navigation (same route, tab state managed internally)

### Pagination
- All 4 list endpoints may return large datasets
- Pagination state per tab: `page`, `size` (default 20)
- Prev/Next buttons + page number buttons + ellipsis for large page counts
- Page size fixed at 20 (no page size selector)

### Loading on Tab Switch
- When switching tabs for the first time, show skeleton loading
- Subsequent switches show cached data immediately
- Refetch on window focus is enabled (default TanStack Query behavior)

### Error Recovery
- If any tab's list query fails, show `<EmptyState>` with "Tải dữ liệu thất bại" and "Thử lại" button
- If a create/update/delete mutation fails, show error toast (not inline error)

### Response Format Note
All list endpoints return a flat JSON array (not paginated wrapper). Pagination UI may be omitted initially depending on actual data volume.

### Delete Conflict
The API may return a 409 Conflict or 422 Validation error when attempting to delete a Transaction Type or Property Type that is referenced by an Organization, or a Tag referenced by a Property. The frontend interprets this as a "cannot delete, in use" error and shows the appropriate toast.
