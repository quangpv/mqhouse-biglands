# Gap Analysis: SC-011 Hot Products Management

## Against: openapi.yaml

---

## Missing API Params

### 1. No `isHot` filter on `GET /listings`
- **Screen**: "Search/select listings to promote" — Admin needs to find CON_HANG listings not already hot and promote them
- **API**: `GET /listings` supports `status` filter but no `isHot` boolean filter
- **Impact**: Admin cannot search for "CON_HANG listings that are not hot yet" without fetching all and filtering client-side
- **Fix**: Add optional `isHot` (boolean) query param to `GET /listings`

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| No `isHot` filter on `GET /listings` | `is_hot: bool \| None` param (alias `isHot`) — Admin can search "CON_HANG listings that are not hot yet" via `?status=CON_HANG&isHot=false` | 2.8 |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Reorderable hot list | `PUT /hot-listings/reorder` | ✓ |
| Remove from hot | `DELETE /listings/{id}/promote` | ✓ |
| Add/promote listing | `POST /listings/{id}/promote` with `hotOrder` | ✓ |
| Max 14 items | `PromoteToHotRequest.hotOrder` max 14 (LST-C08) | ✓ |
| HOT badge on homepage | `Listing.isHot` returned from `GET /hot-listings` | ✓ |
| Admin-only access | `security: BearerAuth` + role check → 403 Forbidden | ✓ |
