# Main Layout (App Shell)

Persistent chrome surrounding all authenticated screens. The app shell is rendered after successful login and consists of: sidebar, topbar, content slot, and global overlays (notification dropdown, user dropdown, logout modal, toast).

---

## 1. Desktop Sidebar

Visible on `lg+` screens (`w-64`), fixed height, scrollable.

### Structure

| Section | Items | Icon |
|---------|-------|------|
| Brand | Logo + "Biglands CRM" | home |
| Hệ thống | Trang chủ, Giỏ hàng, Thông báo, Quản lý người dùng, Cấu hình hệ thống | layout-dashboard, shopping-cart, bell, users, settings |
| Duyệt sản phẩm | Bán, Cho thuê, Sang nhượng (each expandable) | badge-dollar-sign, key-round, git-compare |

Each expandable group (Bán / Cho thuê / Sang nhượng) contains:
| Sub-item | Key suffix |
|----------|-----------|
| Duyệt bài đăng | `-duyet-bai-dang` |
| Báo cọc | `-bao-coc` |
| Hủy cọc | `-huy-coc` |
| Chốt hàng | `-chot-hang` |
| Hết hàng | `-het-hang` |

### API

No explicit API — navigation is client-side. Notification badge counts come from notification APIs (see §4).

### States

#### Idle
- Brand section visible at top
- "Trang chủ" item active by default: `text-primary bg-[#F0F5FF] font-medium`
- All other items: `text-textSecondary`
- Expandable menus collapsed (submenu hidden, chevron `rotate(0deg)`)
- Cart shows count badge (`bg-[#F1F5F9]`), notification shows red badge (`bg-[#EF4444]`)

#### Navigation Click
- `data-route` attribute triggers `navigate(route)`
- Active item gets: `text-primary bg-[#F0F5FF] font-medium`
- Previously active item returns to: `text-textSecondary`

#### Expandable Menu
- Click toggles `.submenu` visibility
- Collapsed: submenu hidden, chevron `rotate(0deg)`, no background
- Expanded: submenu visible, chevron `rotate(180deg)`, parent gets `bg-slate-50/50 rounded-[12px] pb-1`
- Sub-items: `text-textSecondary` default, `text-primary` on hover with `bg-[#F1F5F9]`

---

## 2. Mobile Sidebar (Drawer)

Slide-in drawer from left, visible on screens smaller than `lg`.

### States

#### Hidden (default)
- Sidebar translated off-screen (`-translate-x-full`)
- Backdrop overlay hidden

#### Open
- Backdrop overlay visible: `fixed inset-0 bg-[#0F172A]/40 backdrop-blur-sm z-50`
- Sidebar slides in: `translate-x-0`, `w-72`, `z-50`
- Same navigation structure as desktop sidebar
- Close button (X icon) in header
- Clicking backdrop or navigation item closes drawer

#### Closing
- Sidebar slides out (`-translate-x-full`)
- Backdrop fades out
- Transition: `duration-300 ease-in-out`

---

## 3. Topbar

Horizontal bar (`h-16`, `bg-white`, `border-b`) with page title and action buttons.

### Structure

| Position | Element |
|----------|---------|
| Left | Hamburger button (lg:hidden) + Page title |
| Right | Notification bell (with badge) |
| Right | Divider |
| Right | User avatar + name/role + chevron |

### States

#### Idle
- Page title matches current route (from `routeTitles` map)
- Desktop: `text-h3 font-semibold` (`md:block hidden`)
- Mobile: `text-body font-semibold` (`md:hidden block`)
- Notification bell shows badge count from API
- User area shows avatar, name, role

#### Notification Click
- Toggles notification dropdown visibility
- Closes user dropdown if open
- See §4

#### User Click
- Toggles user dropdown visibility
- Closes notification dropdown if open
- See §5

#### Outside Click
- Any open dropdown closes when clicking outside both the button and the dropdown

---

## 4. Notification Dropdown

Dropdown panel triggered by notification bell in topbar.

### API

```
GET /notifications
Params: { page: 1, size: 20, is_read: null }
```

```
GET /notifications/unread-count
```

```
WebSocket /ws?token={jwt}
Message type: "notification_created" — payload: Notification
```

### States

#### Closed (default)
- Dropdown hidden
- Bell icon visible with badge

#### Open — Loading
- Dropdown visible (`w-80 sm:w-96`, `right-0`)
- Placeholder text or spinner in list area

#### Open — Loaded
- Header: "Thông báo mới" + "Đánh dấu đã đọc" link
- Notification list (max-h-80, scrollable):
  - Unread items: blue dot indicator (`w-2 h-2 rounded-full bg-primary`)
  - Read items: no dot
  - Each item: title, description, relative timestamp
- Footer: "Xem tất cả thông báo" link → navigates to "thong-bao" route

#### Open — Empty
- List area shows empty state text: "Không có thông báo nào"

#### Open — Error
- List area shows: "Không thể tải thông báo"

#### WebSocket — Real-time Update
- On `notification_created`: prepend new notification to list, increment badge count
- Badge count updates reactively

#### Mark all read
- Clicking "Đánh dấu đã đọc" calls `POST /notifications/read-all`
- All unread indicators removed
- Badge count resets to 0

---

## 5. User Dropdown

Dropdown panel triggered by user area in topbar.

### Structure

| Item | Action |
|------|--------|
| User info (name, role) | Visible on mobile only (sm:hidden block) |
| Thông tin cá nhân | Link to profile (TBD route) |
| Divider | — |
| Đăng xuất | Opens logout confirmation modal |

### States

#### Closed (default)
- Dropdown hidden

#### Open
- Dropdown visible (`w-56`, `right-0`)
- Hover states on items

---

## 6. Logout Confirmation Modal

### API
```
POST /auth/logout
Response: { message: "string" }
```

### States

#### Closed (default)
- Modal hidden, `.scale-95` transform applied

#### Open
- Backdrop: `fixed inset-0 bg-[#0F172A]/50 backdrop-blur-sm`
- Modal card: `max-w-sm`, `rounded-[20px]`
- Red logout icon in round container
- Title: "Xác nhận đăng xuất"
- Description: "Bạn có chắc chắn muốn rời khỏi phiên làm việc hiện tại trên hệ thống CRM?"
- Two buttons:
  - "Hủy bỏ" → close modal, no action
  - "Đăng xuất" → confirm logout
- Scale animation: `scale-95 → scale-100` on open, reverse on close

#### Loading
- "Đăng xuất" button shows spinner, both buttons disabled

#### Success
- Close modal
- Navigate to login screen (`navigate('dang-nhap')`)
- Clear stored tokens

#### Error
- Toast: "Đăng xuất thất bại. Vui lòng thử lại."
- Modal closes, user remains logged in

---

## 7. Toast Notification

Global toast for non-blocking feedback messages.

### States

#### Hidden (default)
- `hidden`, `translate-y-10 opacity-0`

#### Visible
- `fixed bottom-6 right-6 z-50`
- White card with blue info icon
- Title: "Thông báo hệ thống"
- Description: contextual message
- Close button (X icon)
- Auto-dismiss after ~3–4 seconds
- Slide up + fade in animation

---

## 8. Router

Client-side routing system mapping route keys to HTML partials.

### Behavior

| Route | Partial Path | View |
|-------|-------------|------|
| `dang-nhap` | `login/login_content.html` | Login (hides app shell) |
| `quen-mat-khau` | `forgot-password/forgot-password_content.html` | Forgot password (hides app shell) |
| `trang-chu` | `home/home_content.html` | Dashboard |
| `gio-hang` | `my-cart/my-cart.html` | My cart |
| `thong-bao` | `notification/notification-content.html` | Notifications |
| `quan-ly-nguoi-dung` | `user-management/user-management-content.html` | User management |
| `chi-tiet-san-pham` | `product-details/product-details-content.html` | Property detail |
| `them-hang` | `create-product/create-product-content.html` | Create property |
| `cau-hinh-he-thong` | `config-system/config-system.content.html` | System config |
| `ban-*`, `thue-*`, `sangnhuong-*` | `review-products/review-products-content.html` | Review products |

### States

#### Initial Load
- On `DOMContentLoaded`, navigate to `dang-nhap`

#### Navigation
- `navigate(route)` called:
  1. Update page title (both desktop + mobile)
  2. Update sidebar active state (`updateSidebarActive`)
  3. For login/forgot-password: show login view, hide app shell
  4. For all other routes: hide login view, show app shell
  5. Load HTML partial into `#page-content` via `fetch`
  6. Execute any inline scripts from partial
  7. Reinitialize Lucide icons

#### Loading Partial
- `fetch(partialUrl)` in progress
- Content area shows previous page content (no loading skeleton for shell)

#### Error Loading Partial
- Show fallback: "Không thể tải nội dung."

#### Unknown Route
- Show template placeholder: "Tính năng đang phát triển" with description

---

## 9. Add Product Modal

Global modal for quick product creation, accessible from multiple screens.

### API
```
POST /properties
Request: CreatePropertyRequest
Response: PropertyResponse
```

### States

#### Closed (default)
- Modal hidden

#### Open
- Backdrop: `fixed inset-0 bg-slate-900/60 backdrop-blur-xs`
- Modal card: `max-w-2xl`, `rounded-[20px]`
- Header: "Thêm Căn Mới Vào Giỏ Hàng" + close button
- Form fields (2-column grid):

  | # | Field | Type | Required |
  |---|-------|------|----------|
  | 1 | Tên bất động sản / Tiêu đề tin đăng | text | yes |
  | 2 | Loại giao dịch | select (Bán, Thuê) | yes |
  | 3 | Loại hình sản phẩm | select (Căn hộ, Biệt thự, Nhà phố, Đất nền) | yes |
  | 4 | Địa chỉ chính xác | text | yes |
  | 5 | Diện tích đất (m²) | number | yes |
  | 6 | Đơn giá ước lượng (triệu/m²) | number | no |
  | 7 | Giá thuê gốc (VNĐ/tháng) | text | no |
  | 8 | Giá bán/chuyển nhượng (VNĐ) | text | no |
  | 9 | Số phòng ngủ | number | no |
  | 10 | Số phòng vệ sinh (WC) | number | no |
  | 11 | Số tầng | number | no |
  | 12 | Trạng thái rổ hàng | select (Còn hàng, Đã cọc, Đã bán) | yes |
  | 13 | Hình ảnh | select (Unsplash presets) | no |
  | 14 | Nhãn đặc thù | text (comma-separated) | no |

- Actions: "Đóng" (cancel), "Lưu thông tin" (submit)

#### Validation Error
- HTML5 validation on required fields
- Toast for API validation errors

#### Submitting
- "Lưu thông tin" button shows spinner
- All fields disabled

#### Success
- Close modal
- Toast: "Bất động sản mới {id} đã được đưa lên rổ hàng."
- Refresh current view

#### Error
- Toast with error message
- Fields remain editable

---

## 10. Product Card Events (Shared)

Global event delegation for product-card interactions across screens.

| Event | Action |
|-------|--------|
| `product-card:select` | Navigate to property detail |
| `product-card:pin` | Toggle pin status |
| `product-card:unpin` | Toggle pin status |
| `product-card:action` (action="hot") | Open hot promotion modal |
| `product-card:action` (action="unhot") | Un-promote hot |
| `product-card:action` (action="edit") | Navigate to edit property |
| `product-card:action` (action="approve") | Approve (approver/admin) |
| `product-card:action` (action="reject") | Reject (approver/admin) |
| `product-card:action` (action="delete") | Delete property |

---

## UI Text Reference

| Context | Vietnamese |
|---------|-----------|
| Brand | Biglands CRM |
| Section: Hệ thống | Hệ thống |
| Section: Duyệt sản phẩm | Duyệt sản phẩm |
| Nav: Trang chủ | Trang chủ |
| Nav: Giỏ hàng | Giỏ hàng |
| Nav: Thông báo | Thông báo |
| Nav: Quản lý người dùng | Quản lý người dùng |
| Nav: Cấu hình hệ thống | Cấu hình hệ thống |
| Nav: Bán | Bán |
| Nav: Cho thuê | Cho thuê |
| Nav: Sang nhượng | Sang nhượng |
| Sub: Duyệt bài đăng | Duyệt bài đăng |
| Sub: Báo cọc | Báo cọc |
| Sub: Hủy cọc | Hủy cọc |
| Sub: Chốt hàng | Chốt hàng |
| Sub: Hết hàng | Hết hàng |
| Notif dropdown header | Thông báo mới |
| Notif mark all read | Đánh dấu đã đọc |
| Notif view all | Xem tất cả thông báo |
| Notif empty | Không có thông báo nào |
| Notif error | Không thể tải thông báo |
| User: Thông tin cá nhân | Thông tin cá nhân |
| User: Đăng xuất | Đăng xuất |
| Logout title | Xác nhận đăng xuất |
| Logout description | Bạn có chắc chắn muốn rời khỏi phiên làm việc hiện tại trên hệ thống CRM? |
| Logout cancel | Hủy bỏ |
| Logout confirm | Đăng xuất |
| Logout error | Đăng xuất thất bại. Vui lòng thử lại. |
| Toast title | Thông báo hệ thống |
| Content error | Không thể tải nội dung. |
| Feature placeholder title | Tính năng đang phát triển |
| Feature placeholder desc | Tính năng này hiện đang được xây dựng và sẽ sớm ra mắt. Vui lòng quay lại sau. |
| Footer version | Hệ thống Biglands CRM v2.4.1 • Hoạt động tốt trên mọi thiết bị |
| Add modal title | Thêm Căn Mới Vào Giỏ Hàng |
| Add: close | Đóng |
| Add: save | Lưu thông tin |
