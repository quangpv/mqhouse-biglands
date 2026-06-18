# My Cart

## Purpose

View the current user's own listings — organized by posting status.

## Route

`/gio-hang`

## Components

### Filter Tabs
- "Đã đăng (N)" — Posted/published listings
- "Chờ duyệt (N)" — Pending approval
- "Từ chối (N)" — Rejected
- "Quá hạn (N)" — Expired

> **Role difference**: Agent sees all 4 tabs. Admin sees only 2 tabs: "Đã đăng" and "Quá hạn" (no Chờ duyệt / Từ chối). This is because admin posts go directly live without approval.

### Search
- Textbox with placeholder: "Mã sản phẩm, tiêu đề, nội dung, địa chỉ"

### "Nhập hàng mới" Button
- Links to `/gio-hang/tao`

### Listing Card (own listings)
- Cover image
- Commission badge (percentage: "50%", "100%", "1%" or fixed amount: "30 triệu")
- Status badge: "Còn hàng" (green) / "Hết hàng" (gray/red)
- Featured tags: "Nhà mới", "Thang máy", "Vị trí đẹp"
- Transaction type + status label
- Title (clickable → listing edit/detail at `/gio-hang/:id`)
- Address
- Price (total) / Area = price per m²
- Area: "width × length = total m²"
- Room count, WC count, floor count
- Poster name, date
- Two management action icon buttons (edit/delete)

### Empty State
- Message: no listings created yet
- "Nhập hàng mới" CTA button

## Entities

- Listing
- ListingImage

## Related Stories

- Listing Management US-001 (create listing), US-002 (edit), US-003 (manage status)

## Navigation Links

- Shared Cart Home `/`
- Create Listing `/gio-hang/tao`
- Product Detail `/gio-hang/:id` (own listing detail)
- Edit Listing `/gio-hang/:id/chinh-sua`
