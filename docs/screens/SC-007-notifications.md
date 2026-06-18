# Notifications

## Purpose

View system notifications: deal events, status changes, and transaction updates.

## Route

`/thong-bao`

## Sidebar

- Notification bell with unread count (e.g., "44")
- Active state when on notifications page

## Components

### Top Banner
- Notification bell icon with unread count badge
- User avatar + name dropdown ("Đăng xuất")

### Page Header
- H1 heading: "Thông báo"

### Scope (role-dependent)
- **Agent**: Sees only their own relevant notifications (observed: 4,397 total, 44 unread for Mr Quân)
- **Admin**: Sees all system-wide notifications (observed: 8,529 total)
- Confirms BR-010 (updated) — notifications are scoped by role

### Filter Tabs
- "Tất cả" (All) / "Chưa đọc" (Unread)
- Category filters:
  - Tất cả loại hàng (total count)
  - BÁN (N)
  - CHO THUÊ (N)
  - SANG NHƯỢNG (N)

### Search
- Textbox with placeholder: "Tìm kiếm"

### Notification List
- Reverse-chronological list
- Each item format:
  `[Transaction type] [User] thông báo [Product code] [event] [timestamp]`
- Event types:
  - "đã hết" — listing marked sold-out / expired
  - "đã chốt cọc" — deposit confirmed (with "thành công" label)
  - "đã chốt hàng" — deal finalized (with "thành công" label)
- Timestamps: e.g., "vài giây trước", "6 giờ trước", "một ngày trước", "2 ngày trước", etc.
- Clickable — links to related listing

### Pagination
- Previous/Next buttons
- Page number buttons
- Multiple pages available (observed: 5+)

## Empty State

- "No notifications" message

## Entities

- Notification

## Related Stories

- Notification System US-001 (receive), US-002 (mark read)

## Navigation Links

- Related Listing `/san-pham/:id` (via notification click)
- Shared Cart Home `/`
