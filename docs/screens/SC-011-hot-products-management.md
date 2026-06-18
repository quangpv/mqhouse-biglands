# Hot Products Management

## Purpose

Manage which listings are promoted with the "HOT" badge on the homepage.

## Route

`/admin/san-pham-hot`

## Components

### Current Hot List
- Reorderable list of promoted listings
- Each item: listing title, image, current position
- Drag to reorder
- "Remove" button per item

### Add Hot Product
- Search/select listings to promote
- Max count limit enforcement

### Homepage Display
- Hot products shown in a dedicated section before the main grid (observed: 14 hot items)
- Items display "🔥 HOT" badge on card

## Entities

- Listing

## Related Stories

- Hot Products US-001 (promote to hot), US-002 (manage hot list)

## Access

- **Admin only**: Visible in sidebar and route accessible
- **Agent**: Not in sidebar; route `/admin/san-pham-hot` returns "Bạn không có quyền truy cập trang này"

## Navigation Links

- Shared Cart Home `/`
- Product Detail `/san-pham/:id`
