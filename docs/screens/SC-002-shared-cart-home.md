# Shared Cart Home

## Purpose

Main deal-pool page where agents browse all available listings.

## Route

`/`

## Components

### Top Banner (above sidebar nav)
- Notification bell icon with unread count badge — links to `/thong-bao`
- "Biglands" branded logo/title toggle button

### Sidebar
- Logo (links to `/`)
- "Trang giỏ hàng chung" (Shared Cart) — active state
- "Giỏ hàng của tôi" (My Cart) — links to `/gio-hang`
- "Thông báo" (Notifications) — links to `/thong-bao`, shows unread count badge

> **Admin sidebar** (full access):
> - "Sản phẩm HOT" (Hot Products) — links to `/admin/san-pham-hot`
> - "Quản lý người dùng" (User Management) — links to `/admin/quan-ly-nguoi-dung`
> - 3 transaction-type accordion menus (BÁN, CHO THUÊ, SANG NHƯỢNG), each with 5 approval queue links showing pending counts
>
> **Agent sidebar** (limited to 3 items):
> - Only "Trang giỏ hàng chung", "Giỏ hàng của tôi", and "Thông báo" are visible
> - Admin-only routes (`/admin/*`) return "Bạn không có quyền truy cập trang này"

### Main Content

#### Page Header
- H1 heading: "Danh sách giỏ hàng chung"

#### Hot Products Section
- Heading: "Sản phẩm Hot" with hot icon
- Horizontal scrollable strip of promoted listing cards
- Displays all items marked HOT (observed: 14 items)
- Appears above the filter tabs and search bar

#### Filters & Search
- Filter tabs: "Tất cả loại hàng (N)" / "Đã ghim (N)" / "Hàng Hot (N)"
- Search textbox with placeholder: "Mã sản phẩm, tiêu đề, nội dung, địa chỉ"
- "Nhập hàng mới" button — links to `/gio-hang/tao`
- Paginated listing card grid

### Listing Card (Shared Cart — read-only browsing)
- Cover image
- HOT badge (if promoted, 🔥 badge)
- Commission badge (percentage or fixed amount)
- Transaction type label + status ("Còn hàng" / "Hết hàng")
- Featured tags: "Nhà mới", "Thang máy", "Vị trí đẹp"
- Title (clickable → product detail `/san-pham/:id`)
- Address
- Price (total) / Area = price per m²
- Area: "width × length = total m²"
- Room count, WC count, floor count
- Poster name, date
- Paginated listing grid with Previous/Next + page numbers

### Pagination
- Previous/Next buttons
- Page number buttons

## Entities

- Listing
- ListingImage

## Related Stories

- Shared Cart Browsing US-001 (browse), US-002 (search), US-003 (filter), US-005 (pin)

## Navigation Links

- Product Detail `/san-pham/:id`
- Create Listing `/gio-hang/tao`
- My Cart `/gio-hang`
- Notifications `/thong-bao`
- Admin pages via sidebar
