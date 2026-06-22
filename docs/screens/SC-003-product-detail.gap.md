# Gap Analysis: SC-003 Product Detail

## Against: openapi.yaml

---

## Missing APIs

### 1. Reviews CRUD
- **Screen**: Full reviews section with text input, image upload (max 10 images), "Gửi đánh giá" button, review list, empty state "Chưa có nhận xét nào"
- **API**: No review endpoints exist in openapi.yaml
- **Required endpoints**:
  - `GET /listings/{id}/reviews` — list reviews for a listing
  - `POST /listings/{id}/reviews` — create a review
  - `DELETE /listings/{id}/reviews/{reviewId}` — delete own review
  - `POST /listings/{id}/reviews/{reviewId}/images` — upload review image
- **Impact**: 50+ lines of UI in the screen spec cannot be implemented
- **Priority**: Must Have (UI exists, visible to all users)
- **Note**: Listed as domain model gap G-01. Business rules for reviews (authorship, moderation, rating range) are undefined — see business-spec MR-01.

### 2. View Count Increment
- **Screen**: Product detail renders `viewCount` on the listing
- **API**: `GET /listings/{id}` returns `viewCount` but no mechanism increments it
- **Impact**: `viewCount` stays 0 forever
- **Fix**: Fire `POST /listings/{id}/views` on page load, or have the server increment on `GET /listings/{id}`

## Missing Fields

### 1. `pricePerM2`
- **Screen**: "Price (total) / Area = price per m²" in both header and key info section
- **Schema**: `Listing` has `price` and `totalArea` but no `pricePerM2`
- **Same gap**: SC-002

### 2. `creator` (embedded agent object)
- **Screen**: Shows "Agent name (poster)" and "Contact phone" (poster's phone)
- **Schema**: `ListingDetailResponse` → `Listing.createdById` is a UUID, not user data
- **Same gap**: SC-002, but more critical here because detail page shows phone too
- **Impact**: To render agent name and phone, client must call `GET /users/{createdById}` on every detail page load
- **Fix**: Add `creator: { id: uuid, fullName: string, phone: string }` to `ListingDetailResponse`

### 3. `ownerPhone` visibility rule
- **Screen**: Owner phone is "hidden behind icon" — user must click to reveal
- **API**: `Listing.ownerPhone` is always returned in the response
- **Impact**: No backend control over phone visibility; hiding is purely client-side CSS. A user who inspects network traffic can see the phone without clicking
- **Fix**: This is a privacy concern — consider returning `ownerPhone` only on explicit user action (or add an `ownerPhone` field that is masked by default, with a separate endpoint to reveal)

## Inconsistent Naming

### 1. Status badges
- **Screen**: "Còn hàng" / "Hết hàng"
- **API**: `CON_HANG` / `HET_HANG`
- **Status**: This is a localization concern, not an API contract issue. The FE maps enum → display text.

## Missing States

### 1. Deal action permission ambiguity (C-03) — Resolved
- **Screen**: "Any agent can report deposit/sold-out/cancellation/closure on any listing, not just their own"
- **Resolution**: BR-004 confirmed — any agent can report on any listing. Owner-only preconditions in user flows overridden.
- **Impact**: None — screen matches final decision.

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| `pricePerM2` | Computed in mapper: `price / totalArea` when `totalArea > 0`; returned on `ListingResponse` | 2.2 |
| `creator` (embedded agent object) | `CreatorInfo` schema with `id`, `fullName`, `phone`; embedded in `ListingResponse`; `selectinload` on detail repo query | 1.2 |
| `ownerPhone` visibility | Backend-controlled via `current_user` check: visible when user is creator, ADMIN, or APPROVER; otherwise hidden. `ownerPhone` is `str \| None`. Original caller (create/update/submit/withdraw) always sees it | 3.2 |
| View Count Increment | Pre-existing — server increments `viewCount` on `GET /listings/{id}` | 2.6 (pre-existing) |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Image gallery | `ListingDetailResponse.images` with `url`, `order`, `isPrimary` | ✓ |
| Product code | `Listing.code` | ✓ |
| HOT badge | `Listing.isHot` | ✓ |
| Commission display | `commissionType` + `commissionValue` | ✓ |
| Area dimensions | `areaWidth`, `areaLength`, `totalArea` | ✓ |
| Address fields | `streetName`, `houseNumber`, `ward`, `district`, `city` | ✓ |
| Property features table | `direction`, `frontageType`, `roadWidth`, `legalStatus`, `furnishing` | ✓ |
| Deal action buttons | 4 POST endpoints exist | ✓ |
| Favourite/pin | `PUT /listings/{id}/pin` / `DELETE /listings/{id}/pin` | ✓ |
| Edit button (owner) | `PUT /listings/{id}` (owner-only per BR-004) | ✓ |
