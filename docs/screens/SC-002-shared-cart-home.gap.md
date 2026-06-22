# Gap Analysis: SC-002 Shared Cart Home

## Against: openapi.yaml

---

## Missing Fields

### 1. `pricePerM2`
- **Screen**: Listing card shows "Price (total) / Area = price per m²"
- **Schema**: `Listing` has `price` and `totalArea` but no computed `pricePerM2`
- **Impact**: Client must compute from two fields; floating-point division may produce inconsistent display values
- **Fix**: Add `pricePerM2: number` (nullable) to `Listing` schema

### 2. `creator` (embedded agent name)
- **Screen**: Listing card shows "Poster name" — the agent who created the listing
- **Schema**: `Listing` returns `createdById` (UUID only)
- **Impact**: Every listing card requires a separate user lookup to display the name; N+1 problem
- **Fix**: Add embedded `creator: { id: uuid, fullName: string, phone: string }` to `Listing` response schema, or pre-fetch a `GET /users?ids=...` map on page load

### 3. Per-filter counts
- **Screen**: Filter tabs show "(N)" counts: "Tất cả loại hàng (N)" / "Đã ghim (N)" / "Hàng Hot (N)"
- **Schema**: `ListingListResponse` → `pagination.totalItems` gives only the current filter's total, not all three
- **Impact**: Three API calls needed to render the tab counts, or counts stale between calls
- **Fix**: Add `filterCounts: { all: int, hot: int, pinned: int }` to `ListingListResponse`

## Missing API Params

### 1. `createdBy` filter
- **Screen**: Shared cart shows all listings; My Cart (SC-006) is a separate page
- **Schema**: `GET /listings` has no `createdBy` filter
- **Impact**: My Cart cannot filter to current user's listings without a dedicated endpoint
- **Fix**: Add optional `createdBy` query param (UUID string, or `"me"` shorthand) to `GET /listings`

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| `pricePerM2` | Computed in mapper: `price / totalArea` when `totalArea > 0`; returned as nullable number on `ListingResponse` | 2.2 |
| `creator` (embedded agent) | `CreatorInfo` schema with `id`, `fullName`, `phone`; embedded in `ListingResponse` paired with `selectinload` on repo queries | 1.2 |
| Per-filter counts | `filterCounts: { all: int, hot: int, pinned: int }` on `ListingListResponse`; computed via `count_active()`, hot/pinned subqueries | 2.3 |
| `createdBy` filter | `created_by` query param (alias `createdBy`, UUID or `"me"` shorthand) on `GET /listings` | 1.1 |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Hot products section | `GET /hot-listings` | ✓ |
| Notification badge | `GET /notifications/unread-count` | ✓ |
| Sidebar queue counts | `GET /approvals/queues` → `pendingCount` | ✓ |
| Search | `GET /listings?q=` | ✓ |
| Filter tabs | `GET /listings?filter=all|hot|pinned` | ✓ |
| Pagination | `page` + `size` params + `Pagination` schema | ✓ |
| Listing card fields | `isHot`, `commissionType`, `commissionValue`, `transactionType`, `status`, `label`, `title`, `address`, `price`, `areaWidth`, `areaLength`, `totalArea`, `numRooms`, `numBathrooms`, `numFloors`, `createdAt` | ✓ |
| Create listing button | FE route `/gio-hang/tao` (no API needed) | ✓ |
