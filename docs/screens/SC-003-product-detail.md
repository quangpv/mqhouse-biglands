# Product Detail

## Purpose

View full details of a single listing and perform deal actions (report deposit, closure, cancellation, sold-out).

## Route

`/san-pham/:id`

## Components

### Top Banner
- Notification bell icon with unread count badge — links to `/thong-bao`
- User avatar + name dropdown ("Đăng xuất")

### Header
- Listing title with HOT badge prefix (if promoted)
- Transaction type badge (SANG NHƯỢNG / CHO THUÊ / BÁN)
- Status badge ("Còn hàng" / "Hết hàng")
- Product code (Mã hàng) — format: YYMMDD + random digits

### Image Gallery
- Primary image (large)
- Image counter (e.g., "1/14")
- Previous/Next navigation buttons
- Image strip below with thumbnails

### Key Info Section
- Price (total + per m²)
- Commission ("Hoa hồng: N triệu" or "N%")
- Area: "width × length = total m²"
- Rooms / bathrooms / floors
- Address (street, ward, district, city)

### Agent & Contact Info
- Agent name (poster)
- Contact phone ("Liên hệ:") — poster's phone number
- Owner phone ("Số điện thoại chủ nhà:") — hidden behind icon
- Listing date ("Ngày đăng:")

### Action Buttons (context-dependent)
- "Báo khách cọc" (Report Deposit) — enabled when Còn hàng
- "Báo hết hàng" (Report Sold-Out) — enabled when Còn hàng
- "Báo khách chốt hàng" (Report Deal Closure) — disabled until deposit reported
- "Báo khách huỷ cọc" (Report Cancellation) — disabled until deposit reported
- Favourite/Share icon buttons

### Description
- Full description text with property details, rental/sale info, pricing breakdown

### Property Features Table ("Đặc điểm bất động sản")
- Mức giá (Price)
- Diện tích (Area)
- Số phòng ngủ (Bedrooms)
- Số phòng tắm, vệ sinh (Bathrooms)
- Số tầng (Floors)
- Hướng nhà (Direction)
- Mặt tiền/Hẻm (Street front / Alley)
- Đường vào (Road width)
- Pháp lý (Legal docs)
- Nội thất (Furniture)

### Reviews Section ("Nhận xét & Đánh giá")
- Text input + image upload button (max 10 images)
- "Gửi đánh giá" button (disabled until content entered)
- List of existing reviews (empty state: "Chưa có nhận xét nào")

### Listings State Machine (per Sales role actions)

```
Còn hàng → (Báo khách cọc) → Đã cọc → (Báo khách chốt hàng) → Đã chốt
                                      → (Báo khách huỷ cọc) → Huỷ cọc
Còn hàng → (Báo hết hàng) → Hết hàng
```

## Entities

- Listing
- ListingImage
- DealEvent

## Related Stories

- Shared Cart Browsing US-004 (view product detail)
- Deposit/Deal Lifecycle US-001 (report deposit), US-003 (report closure), US-004 (report cancellation), US-006 (mark sold-out)

## Navigation Links

- Shared Cart Home `/`
- Edit Listing `/gio-hang/:id/chinh-sua` (if owner)
- Create Listing `/gio-hang/tao`
