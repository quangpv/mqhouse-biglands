# Gap Analysis: SC-006 My Cart

## Against: openapi.yaml

---

## Missing API Params

### 1. No `createdBy` filter on `GET /listings`
- **Screen**: My Cart shows only the current user's own listings, organized by status tabs
- **API**: `GET /listings` has no `createdBy` parameter
- **Impact**: Cannot scope results to current user. Would need to either:
  - Add `?createdBy=me` (client sends request; server resolves to current user's UUID)
  - Add a dedicated `GET /users/me/listings` endpoint
  - Or use `GET /listings` and filter client-side (not viable with pagination)
- **Priority**: Must Have (My Cart is a core navigation destination)

### 2. No multi-status filter
- **Screen**: Filter tabs "Đã đăng (N)" / "Chờ duyệt (N)" / "Từ chối (N)" / "Quá hạn (N)" with counts
- **API**: `GET /listings` accepts a single `status` value. The tabs require querying multiple statuses:
  - "Đã đăng" → CON_HANG + DA_COC
  - "Chờ duyệt" → PENDING_APPROVAL
  - "Từ chối" → DRAFT (with rejection event)
  - "Quá hạn" → QUA_HAN
- **Impact**: Each tab needs a separate API call, or the API needs `status[]` (multi-value) or a `statusGroup` filter
- **Fix**: Support `status=CON_HANG,DA_COC` (comma-separated multi-value), or add `statusGroup` param

## Inconsistent Naming

### 1. "Đã đăng" ambiguity
- **Screen**: "Đã đăng" tab means "published/active" listings
- **API**: Multiple statuses map to "published" — `CON_HANG` (active), `DA_COC` (deposited)
- **Impact**: Single-status filter can't represent the tab. Comma-separated or `statusGroup=published` needed

## Missing States

### 1. Admin tab visibility
- **Screen**: Admin sees only 2 tabs: "Đã đăng" and "Quá hạn" (no "Chờ duyệt" / "Từ chối" because admin posts auto-approve)
- **API**: No mechanism to know which tabs to show — this is a frontend role-based concern, but the API should document that ADMIN listings skip approval

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| No `createdBy` filter | `created_by` param (alias `createdBy`, accepts `"me"`) on `GET /listings` — client sends `?createdBy=me`, server resolves to `current_user.id` | 1.1 |
| No multi-status filter | `status` param changed from single value to `list[str] \| None`, accepts comma-separated values like `CON_HANG,DA_COC` via `Query(default=None)` | 1.3 |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Listing card display | Same as SC-002 (gap for `creator` name and `pricePerM2` applies here too — both resolved) | ✓ |
| Search | `GET /listings?q=` | ✓ |
| Create button | FE route `/gio-hang/tao` | ✓ |
| Edit action | `PUT /listings/{id}` | ✓ |
| Delete action | `DELETE /listings/{id}` | ✓ |
| Pagination | `page` + `size` | ✓ |
