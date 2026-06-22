# Backend Plan — Remaining Work

## Status
All **13 modules** (auth, users, listings, listing_images, deal_events, approvals, notifications, pins, hot_products, user_settings, organizations, reviews) are implemented with entities, facades, tests, and Alembic migrations. No new modules or entities needed.

Remaining work is all **enhancements to existing modules** — missing endpoints, response fields, and query params identified from the 11 screen gap files.

---

## Tier 1 — Must Have (blocks core UI flows)

### 1.1 `createdBy` filter on `GET /listings`
**Files:** `SC-002-shared-cart-home.gap.md`, `SC-006-my-cart.gap.md`
**Module:** `listings`
**Endpoint:** `GET /listings`
**Change:** Add `?createdBy=me` query param that filters listings to those created by the current authenticated user.
**Why:** My Cart page and shared cart/home page separation cannot function without scoping listings to the current user.

### 1.2 `creator` embedded object in Listing response
**Files:** `SC-002-shared-cart-home.gap.md`, `SC-003-product-detail.gap.md`
**Module:** `listings`
**Schema:** `ListingResponse`
**Change:** Add `creator: { id, fullName, phone }` field to listing responses, loaded via relationship (selectinload) to avoid N+1 queries.
**Why:** Every listing card shows the agent's name/phone; currently requires a separate user lookup per listing.

### 1.3 Multi-status filter on `GET /listings`
**Files:** `SC-006-my-cart.gap.md`
**Module:** `listings`
**Endpoint:** `GET /listings`
**Change:** Support `?status=CON_HANG&status=DA_COC` (repeated) for combined status queries.
**Why:** My Cart filter tabs need queries like "Đã đăng" = CON_HANG + DA_COC, "Chờ duyệt" = PENDING_APPROVAL, etc.

---

## Tier 2 — Should Have (important UX completeness)

### 2.1 Forgot / Reset password endpoints
**Files:** `SC-001-login.gap.md`
**Module:** `auth`
**Endpoints:** `POST /auth/forgot-password`, `POST /auth/reset-password`
**Change:** Implement password reset flow with token generation/verification.
**Why:** Login screen shows "Quên mật khẩu?" link but it's a dead click.

### 2.2 `pricePerM2` computed field on listing
**Files:** `SC-002-shared-cart-home.gap.md`, `SC-003-product-detail.gap.md`
**Module:** `listings`
**Schema:** `ListingResponse`
**Change:** Add computed `pricePerM2` field (price / area_total).
**Why:** Displayed on every listing card/detail; currently client computes (inconsistent).

### 2.3 `filterCounts` on listing list response
**Files:** `SC-002-shared-cart-home.gap.md`
**Module:** `listings`
**Schema:** `ListingListResponse`
**Change:** Add `filterCounts: { all, hot, pinned }` to reduce 3 separate API calls for tab badge counts.

### 2.4 Notification query params
**Files:** `SC-007-notifications.gap.md`
**Module:** `notifications`
**Endpoint:** `GET /notifications`
**Change:** Add `?transactionType=...` and `?q=...` (search) query params.
**Why:** Category filter tabs and search box are non-functional without backend support.

### 2.5 Notification response counts
**Files:** `SC-007-notifications.gap.md`
**Module:** `notifications`
**Schema:** `NotificationListResponse`
**Change:** Add `unreadCount` and `categoryCounts` fields to eliminate extra API calls on page load.

### 2.6 `viewCount` auto-increment
**Files:** `SC-003-product-detail.gap.md`
**Module:** `listings`
**Change:** Auto-increment `viewCount` on GET listing detail (or add explicit `POST /listings/{id}/views`).
**Why:** `viewCount` exists in schema and is displayed but stays 0 forever.

### 2.7 `requiresApproval` flag on listing edit
**Files:** `SC-005-edit-listing.gap.md`
**Module:** `listings`
**Endpoint:** `PUT /listings/{id}`
**Change:** Return `requiresApproval: bool` in response so client knows if the edit triggered a re-approval flow.

### 2.8 `isHot` filter on `GET /listings`
**Files:** `SC-011-hot-products-management.gap.md`
**Module:** `listings`
**Endpoint:** `GET /listings`
**Change:** Support `?isHot=true/false` filter.
**Why:** Admin needs to find CON_HANG listings that are not yet promoted to hot.

### 2.9 `dealEvent` + `reportedBy` in approval queue items
**Files:** `SC-008-approval-queue.gap.md`
**Module:** `approvals`
**Schema:** `ApprovalQueueItem`
**Change:** Embed `dealEvent` (customerName, customerPhone, depositAmount, notes) and `reportedBy` (id, fullName) in queue items.

### 2.10 `generatedPassword` on user creation
**Files:** `SC-009-user-management-list.gap.md`, `SC-010-user-create-edit.gap.md`
**Module:** `users`
**Endpoint:** `POST /users`
**Change:** Return `generatedPassword` in 201 response and make `password` optional in request body (auto-generate if omitted).

### 2.11 `ACCOUNT_DEACTIVATED` error on login
**Files:** `SC-001-login.gap.md`
**Module:** `auth`
**Change:** Return distinct error code when a deactivated user tries to log in (currently generic "wrong password").

### 2.12 Image-count validation on listing submit
**Files:** `SC-004-create-listing.gap.md`
**Module:** `listings`
**Endpoint:** `POST /listings/{id}/submit`
**Change:** Reject submission if listing has zero images (BR-007).

---

## Tier 3 — Could Have (nice-to-have)

### 3.1 Date-range and agent filters on approval queues
**Files:** `SC-008-approval-queue.gap.md`
**Module:** `approvals`
**Params:** `createdAfter`, `createdBefore`, `agentId`

### 3.2 `ownerPhone` visibility control
**Files:** `SC-003-product-detail.gap.md`
**Module:** `listings`
**Change:** Mask or conditionally expose owner phone based on user role/permission.

### 3.3 Structured notification fields
**Files:** `SC-007-notifications.gap.md`
**Module:** `notifications`
**Change:** Add `eventType`, `actorName`, `transactionType` structured fields (currently opaque title/body strings).

### 3.4 Transaction type lock semantics
**Files:** `SC-005-edit-listing.gap.md`
**Module:** `listings`
**Change:** Clarify if `transactionType` is write-once or mutable on edit.

---

## Implementation Order

```
Phase 2: Tier 1 (1.1 → 1.2 → 1.3)
Phase 3: Tier 2 (2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7 → 2.8 → 2.9 → 2.10 → 2.11 → 2.12)
Phase 4: Tier 3 (3.1 → 3.2 → 3.3 → 3.4)
```

Each item follows TDD: write test → implement → verify all existing tests still pass.
