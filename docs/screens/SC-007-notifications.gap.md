# Gap Analysis: SC-007 Notifications

## Against: openapi.yaml

---

## Missing API Params

### 1. No `transactionType` filter
- **Screen**: Category filter tabs: "Tất cả loại hàng (N)" / "BÁN (N)" / "CHO THUÊ (N)" / "SANG NHƯỢNG (N)"
- **API**: `GET /notifications` only supports `isRead`, `page`, `size`
- **Impact**: Category tabs cannot be implemented. The notification content (`title`/`body`) embeds transaction type as text, so client-side filtering by text search is fragile
- **Fix**: Add `transactionType` query param (enum: BAN/CHO_THUE/SANG_NHUONG). Also add per-type counts in response, or expose `GET /notifications/counts`

### 2. No `q` (search) parameter
- **Screen**: Search textbox with placeholder "Tìm kiếm"
- **API**: `GET /notifications` has no `q` param
- **Impact**: Client would need to fetch all pages and filter locally (O(n) memory)
- **Fix**: Add optional `q` param for text search across `title` and `body` fields

## Missing Fields

### 1. No `unreadCount` in list response
- **Screen**: Top banner shows unread count badge; screen also shows total count in page header
- **API**: `GET /notifications` returns `data` + `pagination`. Unread count requires a second call to `GET /notifications/unread-count`
- **Impact**: Every notification page load triggers 2 API calls for counts that could be returned in one
- **Fix**: Add `unreadCount: int` to `NotificationListResponse` (alongside `data` and `pagination`)

### 2. No per-category count in list response
- **Screen**: Category filter tabs display counts: "BÁN (N)", "CHO THUÊ (N)", "SANG NHƯỢNG (N)"
- **API**: No category count data in any response
- **Impact**: Requires 4 API calls (all + 3 categories) to render the filter bar
- **Fix**: Add `categoryCounts: { all: int, BAN: int, CHO_THUE: int, SANG_NHUONG: int }` to `NotificationListResponse`

### 3. No structured notification fields
- **Screen**: Notification format `[Transaction type] [User] thông báo [Product code] [event] [timestamp]` — suggests structured data (transactionType, actorName, productCode, eventType)
- **API**: `Notification` schema has opaque `title` (String 500) and `body` (Text) — no structured fields
- **Impact**: Client must parse the title string to extract components for display. Fragile across locales
- **Fix**: Add optional structured fields: `eventType: string`, `actorName: string`, `transactionType: TransactionType` to `Notification`. This is a recommendation, not a blocker.

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| No `transactionType` filter | `transaction_type` param (alias `transactionType`, maps to `ReferenceType` enum) on `GET /notifications` — enables category tab filtering | 2.4 |
| No `q` search param | `q` param on `GET /notifications` — searches across `title` using `ilike` | 2.4 |
| No `unreadCount` in list response | `unread_count: int` field on `NotificationListResponse` alongside `data` and `pagination` | 2.5 |
| No per-category counts | `category_counts: { all, BAN, CHO_THUE, SANG_NHUONG }` on `NotificationListResponse`; computed via `get_category_counts()` repo method | 2.5 |
| No structured notification fields | `event_type`, `actor_name`, `transaction_type` columns added to `NotificationEntity` and exposed on `NotificationResponse` | 3.3 |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Notification list (reverse-chronological) | `GET /notifications` → sorted by `createdAt` desc | ✓ |
| Read/unread filter | `?isRead=true|false` | ✓ |
| Mark as read | `PATCH /notifications/{id}/read` | ✓ |
| Mark all as read | `POST /notifications/read-all` | ✓ |
| Unread badge count | `GET /notifications/unread-count` | ✓ |
| Click → related listing | `Notification.referenceId` + `referenceType` | ✓ |
| Pagination | `page` + `size` | ✓ |
