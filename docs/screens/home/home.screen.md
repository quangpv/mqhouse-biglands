# Home Screen

Trang chủ - Main dashboard for browsing and managing property listings.

---

## 1. Hot Products Section ("Hàng Tiêu Biểu Nổi Bật")

Horizontal scrollable row of promoted (hot) properties.

### API
`GET /properties/hots`

### Response (200)
```json
[
  {
    "id": "uuid",
    "property": { Property },
    "start_time": "2026-06-20T00:00:00",
    "end_time": "2026-06-27T00:00:00",
    "created_by": "uuid",
    "created_at": "2026-06-20T00:00:00"
  }
]
```

### States

#### Loading
- Horizontal scroll area shows skeleton cards (3–4 placeholder cards with shimmer)
- Section heading remains visible

#### Empty
- Entire section hidden (no heading, no scroll area)

#### Error
- Section hidden, error logged silently (non-critical content)

#### Loaded
- Render `<product-card>` for each hot property in a horizontal flex container
- Cards have fixed width synced to grid column width (via `ResizeObserver`)
- Cards support: select (navigate to detail), pin toggle, hot/unhot actions (role-based)

---

## 2. Tab Navigation

Three tabs controlling which subset of properties is displayed.

| Tab | Key | Behavior |
|-----|-----|----------|
| Tất cả | `all` | Show all visible properties (default, active on mount) |
| Đã ghim | `pinned` | Show only pinned properties |
| Hàng hot | `hot` | Show only hot properties |

### States

#### Idle
- Active tab: `bg-white shadow-sm text-primary`
- Inactive tabs: `text-textSecondary`
- Each tab shows count badge: `(<number>)`

#### Switching
- Update active tab visual immediately
- Fetch data for the selected tab (pass `is_hot`, `is_pin`, `created_by` params)
- Reset to page 1
- Show loading state in product grid (see §5 Loading)

---

## 3. Search

### API
`GET /properties?search={query}` (part of `PropertyListParams`)

### Behavior
- Client-side debounce on input (~300ms)
- Placeholder: "Tìm kiếm địa chỉ, tên dự án, khu vực..."
- On input: reset page to 1, fetch filtered results

### States

#### Idle
- Search icon on left, input field ready
- Placeholder text visible when empty

#### Typing
- Debounce before triggering API call
- Show loading state in grid

#### Empty query
- Show all results for current tab/filters

---

## 4. Advanced Filters (CRMFilter)

Toggle-able filter panel with multiple filter types. Clicking the `sliders-horizontal` icon button toggles the panel.

### Filter Fields

| # | Label | Type | Options | API Param |
|---|-------|------|---------|-----------|
| 1 | Hình thức | multi-select dropdown | Bán, Thuê, Sang nhượng | `transaction_type_id` |
| 2 | Loại hình | multi-select with search | Căn hộ, Biệt thự, Nhà phố, Đất nền | `property_type_id` |
| 3 | Nhãn | multi-select with search | Sổ hồng sẵn, Bán nhanh, Hạ giá, Nội thất, Hồ bơi, Sổ đỏ, Mặt tiền, Giá rẻ, Sổ hồng riêng, View sông, Mới bàn giao, Trung tâm | `label` |
| 4 | Quận | multi-select with search | Quận 1, Quận 2, Quận 7, TP. Thủ Đức, Bình Chánh, Bình Thạnh, Nhơn Trạch, Biên Hòa, Cần Giuộc, Củ Chi | `district` |
| 5 | Phường | multi-select with search | Phường Bến Nghé, Thảo Điền, Khu Đô Thị Sala, ... | `ward` |
| 6 | Hướng | multi-select | Đông, Tây, Nam, Bắc | `direction` |
| 7 | Số phòng | multi-select | 1–10 | `room_count` (range) |
| 8 | Diện tích | range input (min/max) | Diện tích tối thiểu / Diện tích tối đa (m²) | `area` (range) |
| 9 | Ngang mặt tiền | range input (min/max) | Ngang tối thiểu / Ngang tối đa (m) | `width` (range) |
| 10 | Trạng thái | multi-select | available, deposited, soldout | `status` |
| 11 | Khoảng giá | range slider (0–100 tỷ) | Giá tối thiểu / Giá tối đa | `price` (range) |

### APIs for filter option sources
- `GET /transaction-types` → populates "Hình thức"
- `GET /property-types` → populates "Loại hình"
- `GET /geography/cities/{city_id}/districts` → populates "Quận"
- `GET /geography/cities/{city_id}/districts/{district_id}/wards` → populates "Phường"

### States

#### Closed (default)
- Panel hidden, filter button shows icon

#### Open
- Panel visible with all filter fields in a 1–4 column grid
- Each field shows a trigger button with current selection summary
- Clicking a trigger opens a popover below

#### Popover open (multi-select)
- Scrollable option list with checkboxes
- Optional search input to filter options
- "Chọn tất cả" / "Bỏ chọn" toggle button
- "Hoàn tất" button to close popover

#### Popover open (range input)
- Two number fields (Tối thiểu / Tối đa)
- "Huỷ" and "Xác nhận" buttons

#### Popover open (range slider)
- Single slider (0–100 tỷ)
- Read-only min/max display
- "Huỷ" and "Xác nhận" buttons

#### Filter Applied
- Trigger button shows selected values
- Product grid updates with filtered results
- Toast: "Đã cập nhật: {value}"

#### Reset
- All filters return to default
- Toast: "Đã thiết lập lại"
- Product grid resets

---

## 5. Product Grid

Responsive card grid showing property results.

### API
`GET /properties`

### Request Params
`PropertyListParams` — includes all filter, search, pagination, sort, and tab params (`is_hot`, `is_pin`, `created_by`)

### Response
`PropertyListResponse` = `{ data: Property[], metadata: PageDTO }`

### States

#### Loading
- Grid area shows 4–8 skeleton cards (gray placeholder rectangles with shimmer)
- Existing cards replaced by skeletons

#### Loaded (with results)
- Render `<product-card>` for each property in a responsive grid:
  - 1 column (sm)
  - 2 columns (sm+)
  - 3 columns (md+)
  - 4 columns (lg+)
- Gap: 24px between cards

#### Empty
- Full empty state shown (see §6)

#### Error
- Toast or inline banner: "Không thể tải danh sách bất động sản"
- Grid shows empty or retry button

---

## 6. Empty State

Shown when no properties match the current filters/tab/search.

### Visual
- Search code icon in a round gray container
- Title: "Không tìm thấy bất động sản phù hợp"
- Description: "Hãy thử thay đổi từ khóa tìm kiếm hoặc làm mới bộ lọc để hiển thị nhiều kết quả hơn."
- Button: "Xóa bộ lọc" — resets all filters, search, switches to "Tất cả" tab

### States

#### Visible
- Product grid hidden
- Empty state centered

#### Hidden (default)
- Product grid visible

---

## 7. Pagination

### API
Built into `GET /properties` via `page` and `size` query params.

### Display
- Text: "Hiển thị {start} - {end} trong số {total} sản phẩm"
- "Trước" button with chevron-left icon
- Page number buttons (1, 2, 3, ...)
- "Sau" button with chevron-right icon
- Active page: `bg-primary text-white`
- Items per page: 10 (default)

### States

#### Visible (total > 0)
- Full pagination bar below grid

#### Hidden (total = 0)
- Entire pagination bar hidden (empty state takes over)

#### First page
- "Trước" disabled

#### Last page
- "Sau" disabled

#### Page click
- Smooth scroll grid into view
- Update page number
- Fetch new page data
- Show loading state in grid

---

## 8. Action: Thêm hàng

### Trigger
Button with `+` icon and "Thêm hàng" text (icon-only on small screens).

### API
Redirects to the property creation flow. Eventually calls `POST /properties` with `CreatePropertyRequest`.

### States

#### Idle
- Button visible in the action bar

#### Clicked
- Navigate to add-property screen

---

## 9. Action: Pin / Unpin

### APIs
- `POST /properties/{id}/pins` → pin
- `DELETE /properties/{id}/pins` → unpin

### States

#### Toggle
- Toggle pin status on product-card
- Toast: "Đã ghim bất động sản" / "Đã bỏ ghim bất động sản"
- Update tab counts (pinned count)
- Refresh current view

---

## 10. Action: Promote to Hot

### API
`POST /properties/{id}/hots`

### Request
```json
{
  "start_time": "2026-06-20",
  "end_time": "2026-06-27"
}
```

### Modal States

#### Closed (default)
- Hot modal hidden

#### Open
- Dimmed backdrop with `backdrop-blur-sm`
- White card (max-w-sm, rounded-[16px])
- Title: "Đẩy lên Hot 🔥"
- Close button (X icon)
- "Ngày bắt đầu" — date input, default: today
- "Ngày kết thúc" — date input, default: today + 7 days
- "Hủy" button → close, no action
- "Xác nhận" button → validate and submit

### Validation Error
- Missing dates: "Vui lòng chọn ngày bắt đầu và kết thúc."
- End before start: "Ngày kết thúc phải sau ngày bắt đầu."

### Success
- Property marked `isHot = true`
- Re-render hot products section
- Refresh current grid
- Toast: "Sản phẩm đã được đẩy lên Hàng Hot 🔥"
- Close modal

---

## 11. Action: Un-hot

### API
`DELETE /properties/{id}/hots`

### States

#### Triggered
- Property marked `isHot = false`
- Remove from hot products section
- Refresh current grid
- Toast: "Sản phẩm đã được gỡ khỏi Hàng Hot."

---

## 12. Product Card Events

Via event delegation:

| Event | Action |
|-------|--------|
| `product-card:select` | Navigate to property detail |
| `product-card:pin` | Toggle pin status |
| `product-card:action` (action="hot") | Open hot modal |
| `product-card:action` (action="unhot") | Un-promote hot |
| `product-card:action` (action="edit") | Navigate to edit property (TBD) |
| `product-card:action` (action="approve") | Approve (approver/admin) |
| `product-card:action` (action="reject") | Reject (approver/admin) |
| `product-card:action` (action="delete") | Delete property |

---

## UI Text Reference

All user-facing strings preserved verbatim:

| Context | Vietnamese |
|---------|-----------|
| Section title | Hàng Tiêu Biểu Nổi Bật |
| Tab: All | Tất cả |
| Tab: Pinned | Đã ghim |
| Tab: Hot | Hàng hot |
| Search placeholder | Tìm kiếm địa chỉ, tên dự án, khu vực... |
| Filter button tooltip | Bộ lọc nâng cao |
| Add button | Thêm hàng |
| Empty title | Không tìm thấy bất động sản phù hợp |
| Empty description | Hãy thử thay đổi từ khóa tìm kiếm hoặc làm mới bộ lọc để hiển thị nhiều kết quả hơn. |
| Empty button | Xóa bộ lọc |
| Pagination text | Hiển thị {start} - {end} trong số {total} sản phẩm |
| Prev | Trước |
| Next | Sau |
| Hot modal title | Đẩy lên Hot 🔥 |
| Start date label | Ngày bắt đầu |
| End date label | Ngày kết thúc |
| Cancel | Hủy |
| Confirm | Xác nhận |
| Select all | Chọn tất cả |
| Deselect all | Bỏ chọn |
| Done | Hoàn tất |
| Filter toast prefix | Bộ lọc |
| Pin toast | Đã ghim bất động sản |
| Unpin toast | Đã bỏ ghim bất động sản |
| Hot success | Sản phẩm đã được đẩy lên Hàng Hot 🔥 |
| Unhot success | Sản phẩm đã được gỡ khỏi Hàng Hot. |
| Add success | Bất động sản mới {id} đã được đưa lên rổ hàng. |
| Filter: Hình thức | Hình thức |
| Filter: Loại hình | Loại hình |
| Filter: Nhãn | Nhãn |
| Filter: Quận | Quận |
| Filter: Phường | Phường |
| Filter: Hướng | Hướng |
| Filter: Số phòng | Số phòng |
| Filter: Diện tích | Diện tích |
| Filter: Ngang mặt tiền | Ngang mặt tiền |
| Filter: Trạng thái | Trạng thái |
| Filter: Khoảng giá | Khoảng giá |
