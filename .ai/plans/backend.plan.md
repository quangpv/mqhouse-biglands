# Backend Implementation Plan — Biglands v1.0

> **Skill**: `backend-patterns` — Async-FastAPI + SQLAlchemy, facade-per-use-case  
> **Base Architecture**: `docs/architecture.md`  
> **Source Documents**: domain-model.md, openapi.yaml, business-spec.md, entities-erd.md, epics/, screens/, user-flows/  
> **Total Endpoints**: 45  
> **Total Facades**: 45  
> **Estimate**: 22–30 days (single developer)

---

## Table of Contents

1. [Implementation Rules](#implementation-rules)
2. [Foundation (Phase 0)](#foundation-phase-0)
3. [Module 1: Auth](#module-1-auth)
4. [Module 2: Users](#module-2-users)
5. [Module 3: Listings](#module-3-listings)
6. [Module 4: Listing Images](#module-4-listing-images)
7. [Module 5: Deal Events](#module-5-deal-events)
8. [Module 6: Approvals](#module-6-approvals)
9. [Module 7: Pins](#module-7-pins)
10. [Module 8: Hot Products](#module-8-hot-products)
11. [Module 9: Notifications](#module-9-notifications)
12. [Module 10: User Settings](#module-10-user-settings)
13. [Deferred Modules](#deferred-modules)
14. [Dependency Graph](#dependency-graph)
15. [Recommended Implementation Order](#recommended-implementation-order)
16. [Freeze Checkpoints](#freeze-checkpoints)
17. [Open Questions & Blockers](#open-questions--blockers)
18. [Module Inventory (Summary)](#module-inventory-summary)

---

## Implementation Rules

1. **Foundation must be implemented first.**
2. **Modules must be implemented one at a time.**
3. **After a module passes validation and tests, mark it as FROZEN.**
4. **Frozen modules must not be modified by later modules unless explicitly approved.**
5. **Later modules may depend on frozen modules but may not refactor them.**
6. Do NOT generate code yet — this document is the implementation plan.
7. Follow the existing backend architecture (`docs/architecture.md`) exactly.
8. Each module uses: `router.py` → `schemas.py` → `mapper.py` → `facades/*.py` → `data/repositories/*.py`
9. Every facade is a single async function in its own file.
10. Every facade outputs a Pydantic response schema (never a raw entity).
11. Errors use typed exception classes from `shared/errors/exceptions.py`.
12. Status transitions are validated against the state machine in `shared/utils/status_machine.py`.
13. Notifications are dispatched via `BackgroundExecutor.enqueue()` — never synchronously.
14. Alembic migrations are additive only (no destructive changes to frozen tables).

---

## Foundation (Phase 0)

**Status:** ✅ Completed & Frozen  
**Dependencies:** None  
**Estimate:** 3–4 days  

### Purpose

Establish the project skeleton: DI container, database connection, auth primitives, error handling, pagination utilities, background executor, and scheduler. No business logic.

### Components

| Component | File | Responsibility |
|-----------|------|----------------|
| App entry | `src/main.py` | `create_app()` → `FastAPI`, module registration |
| Config | `src/platform/config.py` | Pydantic `BaseSettings` from env vars |
| DI | `src/platform/container.py` | Inspect-based `Container` with `Depends()` resolution |
| Database | `src/platform/database.py` | `async_session_factory`, `get_session` dependency |
| Auth infra | `src/platform/auth.py` | `get_current_user`, `require_role` dependencies |
| Security | `src/platform/security.py` | `hash_password()`, `verify()`, JWT `create/decode` |
| Dependencies | `src/platform/dependencies.py` | `get_db`, `get_executor`, `get_scheduler` |
| Logger | `src/platform/logger.py` | `AppLogger` — console + file |
| Background | `src/platform/background.py` | `BackgroundExecutor` (asyncio.Queue) |
| Scheduler | `src/platform/scheduler.py` | `AppScheduler` (APScheduler + lifespan) |
| Base entity | `src/data/entities/_base.py` | `DeclarativeBase` + common mixins (timestamps, UUID PK) |
| Exceptions | `src/shared/errors/exceptions.py` | 6 exception classes (BadRequest, Unauthorized, etc.) |
| Pagination | `src/shared/pagination/__init__.py` | `PaginationParams`, `PaginatedResponse`, `paginate()` |
| Status machine | `src/shared/utils/status_machine.py` | `STATUS_TRANSITIONS` map, `validate_transition()` |
| Code generator | `src/shared/utils/code_generator.py` | `generate_product_code()` (YYMMDD + 7 random digits) |

### Files to Create

```
src/__init__.py
src/main.py
src/platform/__init__.py
src/platform/config.py
src/platform/container.py
src/platform/database.py
src/platform/auth.py
src/platform/security.py
src/platform/dependencies.py
src/platform/logger.py
src/platform/background.py
src/platform/scheduler.py
src/data/__init__.py
src/data/entities/__init__.py
src/data/entities/_base.py
src/shared/__init__.py
src/shared/errors/__init__.py
src/shared/errors/exceptions.py
src/shared/pagination/__init__.py
src/shared/utils/__init__.py
src/shared/utils/status_machine.py
src/shared/utils/code_generator.py
```

**Total: ~23 files**

### Database Changes (Alembic)

1. Initialize Alembic: `alembic init alembic`
2. Configure `alembic/env.py` to use `DATABASE_URL` from config
3. Create seed migration that creates all 8 tables:
   - `users`
   - `listings`
   - `listing_images`
   - `deal_events`
   - `approvals`
   - `notifications`
   - `user_pins`
   - *(Review and ReviewImage deferred)*
4. Seed data: one ADMIN user for initial login

### Tests Required

| Type | Scope |
|------|-------|
| Unit | DI container registration, config loading from env, JWT encode/decode, password hash + verify, pagination helper edge cases, status map integrity, product code format + uniqueness within microsecond |
| Integration | DB session lifecycle (connect → execute → close), Alembic migration up/down, BackgroundExecutor enqueue/dequeue/retry |
| Security | Password hash never equals plaintext, JWT tampering detected, SQLAlchemy session isolation |

### Risks

| Risk | Mitigation |
|------|------------|
| Alembic auto-generation may produce wrong FK names | Manually review migration before applying |
| `BackgroundExecutor` asyncio.Queue may block on shutdown | Add graceful shutdown with `asyncio.wait_for` and timeout |
| `inspect`-based DI may fail on complex types | Test container resolution for all dependencies before building modules |

### Missing Information

- `EXPIRATION_DAYS` config value (default: 30 — needs confirmation from product)
- `SECRET_KEY` management (env var assumed: `BIGLANDS_SECRET_KEY`)
- Image storage backend (local filesystem vs S3) — affects `ListingImage.url` generation
- Logging level and format

---

## Module 1: Auth

**Status:** ✅ Completed & Frozen  
**Dependencies:** Foundation  
**Estimate:** 1–2 days  

### Purpose

User authentication: login (JWT issuance), logout (stateless no-op), and current-user profile retrieval.

### Stories Included

- FL-001-authentication (user-flow)

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/auth/login` | `login` |
| POST | `/auth/logout` | `logout` |
| GET | `/auth/me` | `get_current_user` |

### Entities Used

- `UserEntity` (read in login facade, read in get_current_user)

### Dependencies

- Foundation (platform/auth.py, platform/security.py, UserRepo)

### Files to Create

```
src/data/entities/user.py          # UserEntity — all fields including notification_prefs JSONB
src/data/repositories/__init__.py
src/data/repositories/user_repo.py # get, get_by_username, count_active_admins, list_by_ids
src/modules/__init__.py
src/modules/auth/__init__.py       # module() function
src/modules/auth/router.py         # 3 routes + Depends guards
src/modules/auth/schemas.py        # LoginRequest, LoginResponse
src/modules/auth/mapper.py         # user_to_response(UserEntity) → User schema
src/modules/auth/facades/__init__.py
src/modules/auth/facades/login.py
src/modules/auth/facades/logout.py
src/modules/auth/facades/get_current_user.py
```

**Total: ~12 files**

### Files to Modify

- `src/main.py` — register `auth` module in `MODULES` list

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 5 | Login: valid credentials → JWT returned; wrong password → 401; deactivated user → 401; missing user → 401; JWT decode in get_current_user |
| Integration | 3 | Login flow (POST → JWT → GET /me); logout (204); expired/ invalid token rejected |
| Security | 4 | Brute-force readiness (login rate-limit stub), password comparison timing (constant-time), JWT tampering (bad signature → 401), token not in URL params |

### Freeze Criteria

- All unit tests pass
- All integration tests pass
- No open audit findings

### Risks

| Risk | Mitigation |
|------|------------|
| Token revocation: logout is stateless (no token blacklist) | Acceptable for v1; add JWT blacklist (Redis/DB) in v2 |
| No refresh token mechanism | 24h expiry is sufficient for v1; consider refresh tokens in v2 |

### Missing Information

- Rate limiting policy for login endpoint (recommend: 5 attempts/min per IP, not defined in spec)

---

## Module 2: Users

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth  
**Estimate:** 2–3 days  

### Purpose

Admin-only CRUD for user accounts: create, list (with search/filter/pagination), get, update, deactivate, reactivate, assign role. Includes last-admin invariant protection.

### Stories Included

- US-001-create-user, US-002-edit-user, US-003-deactivate-user, US-004-assign-role

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/users` | `create_user` |
| GET | `/users` | `list_users` |
| GET | `/users/{id}` | `get_user` |
| PUT | `/users/{id}` | `update_user` |
| PATCH | `/users/{id}/deactivate` | `deactivate_user` |
| PATCH | `/users/{id}/reactivate` | `reactivate_user` |
| PATCH | `/users/{id}/role` | `assign_role` |

### Entities Used

- `UserEntity`

### Dependencies

- Auth (role guard: `require_admin`)

### Files to Create

```
src/modules/users/__init__.py
src/modules/users/router.py         # 7 routes + dependency guards
src/modules/users/schemas.py        # CreateUserRequest, UpdateUserRequest, AssignRoleRequest, UserListResponse
src/modules/users/mapper.py         # user_to_response()
src/modules/users/facades/__init__.py
src/modules/users/facades/create_user.py
src/modules/users/facades/list_users.py
src/modules/users/facades/get_user.py
src/modules/users/facades/update_user.py
src/modules/users/facades/deactivate_user.py
src/modules/users/facades/reactivate_user.py
src/modules/users/facades/assign_role.py
```

**Total: ~12 files**

### Files to Modify

- `src/main.py` — register `users` module

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 14 | Create: valid (with AGENT/APPROVER/ADMIN role), duplicate username (409), missing required fields (400); List: pagination, search by name/username/phone, filter by role, filter by isActive; Update: partial fields, not found (404); Deactivate: self (409), last admin (409), normal user (200); Reactivate: already active (200 idempotent); Role: last admin → 409, valid → 200, invalid role → 400 |
| Integration | 7 | Full CRUD flow; deactivation → login blocked → reactivation → login works; role change → permission change on next request |
| Security | 5 | Non-admin 403 on all 7 endpoints; cannot deactivate self; cannot change own role if last admin; username enumeration timing (not critical) |
| API | 14 | Per endpoint: 200/201, 400, 401, 403, 404, 409 where applicable |

### Freeze Criteria

- All unit/integration/security tests pass
- Last-admin invariant verified with automated test (2 admins → deactivate one → try deactivating last)
- API contract matches openapi.yaml for all 7 endpoints

### Risks

| Risk | Mitigation |
|------|------------|
| Last-admin invariant race condition (concurrent role changes) | Use DB-level count query + lock within transaction |
| Username uniqueness race condition | PostgreSQL unique constraint on `username` column + catch `IntegrityError` in facade |
| Deactivated user's listings remain visible but can't create (UM-005) | Add `is_active` check in `listing_create` facade (handled later in Listings module) |

### Missing Information

- Password generation strategy on create (random alphanumeric string? admin-specified?)
- SC-010 says "initial password shown once" — does backend generate it or does admin type it? (Assume admin types it, field is required in CreateUserRequest.)

---

## Module 3: Listings

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Users  
**Estimate:** 4–5 days  

### Purpose

Full listing CRUD, submit/withdraw actions, browse with search/filter/pagination, product detail with embedded images and deal events. This is the central module with the most business logic.

### Stories Included

- US-001-create-listing, US-002-edit-listing, US-003-manage-listing-status
- US-001-browse-listings, US-002-search-listings, US-003-filter-listings, US-004-view-product-detail
- LV-001 through LV-004 (visibility rules)

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/listings` | `create_listing` |
| GET | `/listings` | `list_listings` |
| GET | `/listings/{id}` | `get_listing` |
| PUT | `/listings/{id}` | `update_listing` |
| DELETE | `/listings/{id}` | `delete_listing` |
| POST | `/listings/{id}/submit` | `submit_listing` |
| POST | `/listings/{id}/withdraw` | `withdraw_listing` |

### Entities Used

- `ListingEntity`, `ListingImageEntity` (validate image count on submit)
- `DealEventEntity` (list on product detail)
- `UserPinEntity` (check pinned status for current user on browse)

### Dependencies

- Auth (role guards: `require_agent`, `require_approver`, `require_admin`)
- Users (for `createdById` mapping in detail response)

### Files to Create

```
src/data/entities/listing.py           # ListingEntity — all 35 fields
src/data/entities/listing_image.py     # ListingImageEntity — 5 fields
src/data/repositories/listing_repo.py  # get, get_by_code, list (with dynamic filters), create, update, delete, count_active, list_hot, increment_view_count, list_expired
src/data/repositories/listing_image_repo.py
src/modules/listings/__init__.py
src/modules/listings/router.py         # 7 routes
src/modules/listings/schemas.py        # CreateListingRequest, UpdateListingRequest, Listing, ListingDetailResponse, ListingListResponse
src/modules/listings/mapper.py         # listing_to_response(), listing_to_detail_response()
src/modules/listings/facades/__init__.py
src/modules/listings/facades/create_listing.py
src/modules/listings/facades/list_listings.py
src/modules/listings/facades/get_listing.py
src/modules/listings/facades/update_listing.py
src/modules/listings/facades/delete_listing.py
src/modules/listings/facades/submit_listing.py
src/modules/listings/facades/withdraw_listing.py
```

**Total: ~17 files**

### Files to Modify

- `src/main.py` — register `listings` module
- `src/data/repositories/user_repo.py` — ensure `list_by_ids()` exists for creator resolution

### Database Changes

- Add `listings` table migration (35 columns, FKs to users)
- Add `listing_images` table migration (5 columns, FK to listings)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 22 | Create: save→DRAFT, submit→PENDING_APPROVAL, admin→CON_HANG, deactivated user→403, code auto-generation; List: search by q, filter by transactionType/status/filter tab, sort by createdAt/price/viewCount, pagination, totalCount aggregation; Detail: listing + images + dealEvents + isPinned; Update: DRAFT fields changed in-place, CON_HANG price/area triggers re-approval, non-key fields no re-approval, non-owner→403; Delete: DRAFT→204, CON_HANG→409; Submit: DRAFT→PENDING_APPROVAL, image count check→400 if 0, wrong status→409; Withdraw: CON_HANG→DRAFT, DRAFT→409 |
| Integration | 10 | Full lifecycle (create→draft→add image→submit→approve→edit→withdraw→delete); search across code/title/description/address; filter: hot listings show first; pinned filter returns only user's pins |
| Security | 6 | Non-owner edit blocked; deactivated user create blocked; Approver can browse but not create; browse returns only CON_HANG + DA_COC (LV-001); expired listings hidden; deleted listings 404 |
| API | 14 | Per endpoint + extra: POST 201/400/401/403; GET 200/401; PUT 200/400/401/403/404; DELETE 204/401/403/404/409 |

### Freeze Criteria

- All listing CRUD tests pass
- Search returns correct results across all searchable fields
- Re-approval triggers correct status change on CON_HANG listings
- Admin auto-approve (skip PENDING_APPROVAL) works
- Image count validated on submit (≥1 required)

### Key Algorithms

#### `create_listing` facade

```python
# Pseudo-code
listing = build_entity(data, created_by_id=current_user.id)
if data.action == "submit":
    listing.status = PENDING_APPROVAL
if current_user.role == ADMIN:
    listing.status = CON_HANG
    listing.approved_by_id = current_user.id
    listing.approved_at = now()
listing = await listing_repo.create(listing)
if listing.status == PENDING_APPROVAL:
    executor.enqueue(notify_approvers, listing_id=listing.id)
return listing_to_response(listing)
```

#### `list_listings` facade

```python
# Base filter: status IN (CON_HANG, DA_COC) for shared cart
# If current user is listing owner, return all statuses
# Apply: q (search), transactionType, status, filter (all/hot/pinned), sortBy, sortOrder
# Return: data[], pagination, totalCount (CON_HANG count across all types)
```

#### `update_listing` — re-approval trigger

```python
REAPPROVAL_FIELDS = {"price", "area_width", "area_length", "total_area"}
if old.status == CON_HANG and any(f in changes for f in REAPPROVAL_FIELDS):
    existing.status = PENDING_APPROVAL
```

### Risks

| Risk | Mitigation |
|------|------------|
| `list_listings` has 8 filter params → complex SQL | Builder pattern: `ListingQueryBuilder` with `where()`, `order_by()`, `paginate()` methods |
| Submit + image upload is 2-step — race condition | `submit_listing` validates `image_repo.count_by_listing(id) > 0` inside transaction |
| Search with `ILIKE %...%` slow on >10k listings | Add GIN/trigram index on (title, description, address, code) |

### Missing Information

- `viewCount` increment mechanism (see openapi.yaml: field exists, no endpoint increments it). Decision needed: auto-increment on GET, or separate `POST /listings/{id}/views`?
- `TU_CHOI` status: appears in domain model field list but is not a real status in the state machine — it represents the state after rejection (listing returns to DRAFT). Remove from enum or map to DRAFT.
- Image count enforcement on delete: if only image left and listing is PENDING_APPROVAL, should the image be deletable? (Assume yes — no validation on delete.)

---

## Module 4: Listing Images

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings  
**Estimate:** 1–2 days  

### Purpose

Image upload, delete, reorder, and primary image management for listings. Ownership-guarded (listing owner only).

### Stories Included

- Covered by US-001-create-listing (upload), US-002-edit-listing (manage)

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/listings/{id}/images` | `upload_image` |
| PUT | `/listings/{id}/images/reorder` | `reorder_images` |
| DELETE | `/listings/{listingId}/images/{imageId}` | `delete_image` |
| PUT | `/listings/{listingId}/images/{imageId}/primary` | `set_primary_image` |

### Entities Used

- `ListingImageEntity`, `ListingEntity` (ownership guard)

### Dependencies

- Listings (listing must exist, ownership check)

### Files to Create

```
src/modules/listing_images/__init__.py
src/modules/listing_images/router.py         # 4 routes
src/modules/listing_images/schemas.py         # ReorderImagesRequest
src/modules/listing_images/mapper.py          # image_to_response()
src/modules/listing_images/facades/__init__.py
src/modules/listing_images/facades/upload_image.py
src/modules/listing_images/facades/delete_image.py
src/modules/listing_images/facades/set_primary_image.py
src/modules/listing_images/facades/reorder_images.py
```

**Total: ~9 files**

### Files to Modify

- `src/main.py` — register `listing_images` module

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 8 | Upload: JPEG/PNG/WEBP accepted, >10MB rejected, max 20 enforced (409); Delete: owner OK, non-owner 403, primary image removed (no primary left); Set primary: existing primary reset, new primary set; Reorder: sequence updated |
| Integration | 4 | Upload + download URL access; reorder; delete cascade on listing delete; primary toggle |
| Security | 3 | Non-owner upload → 403; deactivated user upload → 403; image count enforcement can't be bypassed |
| API | 8 | Per endpoint + 409 on max images + 400 on invalid file type |

### Risks

| Risk | Mitigation |
|------|------------|
| Image storage backend undefined (local vs S3) | Abstract behind `ImageStorage` interface; local FS for dev (`UPLOAD_DIR`), S3 adapter later |
| Image deletion from CON_HANG triggers re-approval (ES-002) but screen says "removing primary image" — only primary removal triggers it? | Check: ES-002 says "images" as a category. Assume any image deletion on CON_HANG triggers re-approval. |

### Missing Information

- Max file size (assume 10MB from openapi.yaml)
- Image processing (thumbnails? auto-resize?)
- File naming convention (UUID-based to prevent collisions)

---

## Module 5: Deal Events

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings  
**Estimate:** 2–3 days  

### Purpose

Four deal event reporting endpoints. Any authenticated user (any agent, no owner restriction — C-03 resolved) can report events. Events are immutable; confirmed events are created by the Approvals module.

### Stories Included

- US-001-report-deposit, US-003-report-deal-closure, US-004-report-cancellation, US-006-mark-sold-out

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/listings/{id}/deal-events/deposit` | `report_deposit` |
| POST | `/listings/{id}/deal-events/closure` | `report_closure` |
| POST | `/listings/{id}/deal-events/cancellation` | `report_cancellation` |
| POST | `/listings/{id}/deal-events/sold-out` | `report_sold_out` |

### Entities Used

- `DealEventEntity`, `ListingEntity` (status validation)

### Dependencies

- Listings (listing must exist, status must match expected)

### Files to Create

```
src/data/entities/deal_event.py           # DealEventEntity — 11 fields
src/data/repositories/deal_event_repo.py  # get_pending_confirmation, has_active_deposit, get_by_listing
src/modules/deal_events/__init__.py
src/modules/deal_events/router.py         # 4 routes
src/modules/deal_events/schemas.py        # ReportDepositRequest, ReportClosureRequest, ReportCancellationRequest, ReportSoldOutRequest
src/modules/deal_events/mapper.py         # deal_event_to_response()
src/modules/deal_events/facades/__init__.py
src/modules/deal_events/facades/report_deposit.py
src/modules/deal_events/facades/report_closure.py
src/modules/deal_events/facades/report_cancellation.py
src/modules/deal_events/facades/report_sold_out.py
```

**Total: ~11 files**

### Files to Modify

- `src/main.py` — register `deal_events` module

### Database Changes

- Add `deal_events` table migration (FK → listings, FKs → users)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 12 | Deposit: CON_HANG→201, wrong status→409, duplicate active deposit→409, missing customerName→400, depositAmount=0→400; Closure: DA_COC→201, CON_HANG→409; Cancellation: DA_COC→201, missing reason→400; Sold-out: CON_HANG→201, DA_COC→409 |
| Integration | 4 | Report deposit → listing stays CON_HANG (C-02 resolved: no immediate status change); event appears in deal_events list |
| Security | 4 | Any agent can report on any listing (not just own) — C-03 confirmed; unauthenticated→401 |
| API | 8 | Per endpoint: 201, 400, 401, 403, 404, 409 |

### Key Business Rules (Enforced in Facades)

```python
# report_deposit
validate_transition(listing.status, None)  # status does NOT change
validate_required("customer_name", data.customer_name, min_length=2)
validate_positive("deposit_amount", data.deposit_amount)
if await deal_event_repo.has_active_deposit(listing.id):
    raise ConflictError(code="DUPLICATE_DEPOSIT")

# report_closure
if listing.status != ListingStatus.DA_COC:
    raise ConflictError(code="INVALID_STATUS_TRANSITION")

# report_cancellation
if listing.status != ListingStatus.DA_COC:
    raise ConflictError(code="INVALID_STATUS_TRANSITION")
if not data.reason:
    raise BadRequestError("Cancellation reason is required")

# report_sold_out
if listing.status != ListingStatus.CON_HANG:
    raise ConflictError(code="INVALID_STATUS_TRANSITION")
```

### Freeze Criteria

- All 4 event types validatable against listing status
- Duplicate deposit blocked (DE-I02)
- Cancellation reason required (DD-005)
- Immutable event constraint verified (no update/delete endpoint exposed)

### Risks

| Risk | Mitigation |
|------|------------|
| Concurrent deposit reports on same listing | `has_active_deposit()` check + DB transaction; use `SELECT FOR UPDATE` on listing row |
| Immutable events must never be updated | No update endpoint; events are append-only. If data is wrong, create a new correction event (out of scope) |

### Missing Information

- C-02/C-09 confirmed: deposit report does NOT change status (listing stays CON_HANG until approver confirms). Confirm this is correct before implementation.

---

## Module 6: Approvals

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings, Deal Events  
**Estimate:** 4–5 days  

### Purpose

Approval queue management: list queues (15 total), list queue items, approve/reject individual items, bulk approve listing posts. This is the most complex module — it handles the state machine transitions and creates DealEvents for confirmations.

### Stories Included

- US-001-approve-listing-post, US-002-reject-listing-post, US-003-bulk-approve
- US-002-approve-deposit, US-005-approve-cancellation

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| GET | `/approvals/queues` | `list_queues` |
| GET | `/approvals/queues/{queueType}` | `list_queue_items` |
| GET | `/approvals/{id}` | `get_approval` |
| POST | `/approvals/{id}/approve` | `approve_item` |
| POST | `/approvals/{id}/reject` | `reject_item` |
| POST | `/approvals/bulk-approve` | `bulk_approve` |

### Entities Used

- `ApprovalEntity`, `ListingEntity` (status transition), `DealEventEntity` (confirming events on approve)

### Dependencies

- Listings (status transitions)
- Deal Events (approve deposit reads the pending `DEPOSIT_REPORTED` event)

### Files to Create

```
src/data/entities/approval.py             # ApprovalEntity — 7 fields
src/data/repositories/approval_repo.py    # get_queue_counts, list_queue_items, get_by_listing_and_type, count_pending
src/modules/approvals/__init__.py
src/modules/approvals/router.py           # 6 routes
src/modules/approvals/schemas.py          # ApprovalQueuesResponse, ApprovalQueueItemListResponse, RejectRequest, BulkApproveRequest, BulkApproveResponse
src/modules/approvals/mapper.py           # approval_to_response(), queue_item_to_response()
src/modules/approvals/facades/__init__.py
src/modules/approvals/facades/list_queues.py
src/modules/approvals/facades/list_queue_items.py
src/modules/approvals/facades/get_approval.py
src/modules/approvals/facades/approve_item.py
src/modules/approvals/facades/reject_item.py
src/modules/approvals/facades/bulk_approve.py
```

**Total: ~12 files**

### Files to Modify

- `src/main.py` — register `approvals` module

### Database Changes

- Add `approvals` table migration (FK → listings, FK → users)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 18 | List queues: returns 15 items with pending counts; List queue items: paginated, filterable by transactionType; Approve: each of 5 types (listing_post→CON_HANG, deposit→DA_COC, closure→DA_CHOT, cancellation→CON_HANG, sold-out→HET_HANG); Reject: each type returns to correct previous status; Already processed→409; Wrong listing status→409; Bulk approve: 1/multiple/all selected; Bulk approve with already-processed items (skipped) |
| Integration | 8 | Full flow: listing submitted → queue item appears → approve → status changes → queue item gone; deposit reported → queue → approve → DA_COC + DealEvent confirmed; reject → listing returns to previous status; bulk approve 5 items |
| Security | 6 | Agent 403 on all endpoints; rejection reason required (400); concurrent double-approve (first wins); approval of another approver's item (should work — anyone with APPROVER role can decide) |
| API | 12 | Per endpoint + queueType enum validation + transactionType query param |

### Key Business Rules (Enforced in `approve_item` Facade)

```python
APPROVED_STATUS_MAP = {
    ApprovalType.LISTING_POST: ListingStatus.CON_HANG,
    ApprovalType.DEPOSIT: ListingStatus.DA_COC,
    ApprovalType.CLOSURE: ListingStatus.DA_CHOT,
    ApprovalType.CANCELLATION: ListingStatus.CON_HANG,
    ApprovalType.SOLD_OUT: ListingStatus.HET_HANG,
}

REJECTED_STATUS_MAP = {
    ApprovalType.LISTING_POST: ListingStatus.DRAFT,
    ApprovalType.DEPOSIT: ListingStatus.CON_HANG,
    ApprovalType.CLOSURE: ListingStatus.DA_COC,
    ApprovalType.CANCELLATION: ListingStatus.DA_COC,
    ApprovalType.SOLD_OUT: ListingStatus.CON_HANG,
}
```

### Freeze Criteria

- All 15 queues functional with correct pending counts
- Approve/reject correctly updates listing status per `APPROVED_STATUS_MAP`/`REJECTED_STATUS_MAP`
- Concurrent double-approve: first wins, second gets 409
- Bulk approve works for LISTING_POST only
- Notification triggered on each approve/reject (via BackgroundExecutor)

### Risks

| Risk | Mitigation |
|------|------------|
| `approve_item` mutates 3 entities (Approval, Listing, DealEvent for deposit) | Single DB transaction with `SELECT FOR UPDATE` on approval row |
| Queue counts drift if items are added while listing counts | Count query fetches real-time; acceptable for v1 |
| Bulk approve is scoped to LISTING_POST only (AR-08) | Parameterized; if other types are needed later, add a `type` filter |

### Missing Information

- AR-08: confirmed — bulk approve is listing-post only. Enforce in `router.py` by adding bulk-approve only on listing-post queue items, or accept any type and reject non-listing-post items.

---

## Module 7: Pins

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings  
**Estimate:** 1 day  

### Purpose

Per-user pinning of listings. Idempotent toggle operations. Replaces the ERD's `Listing.isPinned` boolean with a join table.

### Stories Included

- US-005-pin-listings

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| PUT | `/listings/{id}/pin` | `pin_listing` |
| DELETE | `/listings/{id}/pin` | `unpin_listing` |
| GET | `/users/me/pins` | `list_my_pins` |

### Entities Used

- `UserPinEntity`, `ListingEntity` (for list_my_pins response)

### Dependencies

- Listings (listing must exist for pin/unpin)

### Files to Create

```
src/data/entities/user_pin.py              # UserPinEntity — composite PK
src/data/repositories/user_pin_repo.py     # get_by_user_and_listing, list_by_user (paginated)
src/modules/pins/__init__.py
src/modules/pins/router.py                 # 3 routes
src/modules/pins/schemas.py                # (reuses ListingListResponse for list_my_pins)
src/modules/pins/mapper.py                 # user_pin_to_response()
src/modules/pins/facades/__init__.py
src/modules/pins/facades/pin_listing.py
src/modules/pins/facades/unpin_listing.py
src/modules/pins/facades/list_my_pins.py
```

**Total: ~10 files**

### Files to Modify

- `src/main.py` — register `pins` module

### Database Changes

- Add `user_pins` table migration (composite PK, FKs to users and listings)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 5 | Pin: new pin created, re-pin is no-op; Unpin: existing pin removed, re-unpin is no-op; List my pins: paginated, returns Listing[] not UserPin[] |
| Integration | 3 | Pin → appears in list → disappears on unpin; pin counter in listing grid |
| API | 6 | Per endpoint + 404 on bad listing ID |

### Risks

| Risk | Mitigation |
|------|------------|
| Composite PK prevents duplicates naturally | No risk |
| `list_my_pins` needs to return Listing data with `isPinned = true` | Join UserPin → Listing; add `is_pinned: true` to response |

---

## Module 8: Hot Products

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings  
**Estimate:** 1–2 days  

### Purpose

Admin management of hot/promoted listings. Only CON_HANG listings can be promoted. Max 14 hot items.

### Stories Included

- US-001-promote-to-hot, US-002-manage-hot-list

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| POST | `/listings/{id}/promote` | `promote_to_hot` |
| DELETE | `/listings/{id}/promote` | `unpromote_from_hot` |
| GET | `/hot-listings` | `get_hot_listings` |
| PUT | `/hot-listings/reorder` | `reorder_hot_listings` |

### Entities Used

- `ListingEntity` (is_hot, hot_order fields)

### Dependencies

- Listings (listing must exist, must be CON_HANG)

### Files to Create

```
src/modules/hot_products/__init__.py
src/modules/hot_products/router.py         # 4 routes
src/modules/hot_products/schemas.py         # PromoteToHotRequest, ReorderHotListingsRequest
src/modules/hot_products/mapper.py          # listing_to_hot_response()
src/modules/hot_products/facades/__init__.py
src/modules/hot_products/facades/promote_to_hot.py
src/modules/hot_products/facades/unpromote_from_hot.py
src/modules/hot_products/facades/get_hot_listings.py
src/modules/hot_products/facades/reorder_hot_listings.py
```

**Total: ~9 files**

### Files to Modify

- `src/main.py` — register `hot_products` module

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 8 | Promote: CON_HANG→200, non-CON_HANG→409, max 14→409, already hot→200 idempotent; Unpromote: isHot→false, hotOrder→null; List: sorted by hotOrder; Reorder: positions updated, duplicate order→400 |
| Integration | 3 | Promote → appears in GET /hot-listings → unpromote → gone; reorder → order changed |
| Security | 3 | Admin-only: non-admin 403 on promote/unpromote/reorder; GET /hot-listings returns 200 for all roles |

### Risks

| Risk | Mitigation |
|------|------------|
| 14 hot items limit is an observed value (AR-06), not a hard business rule | Make `MAX_HOT_ITEMS` configurable via settings (default 14) |
| `hotOrder` uniqueness on reorder — concurrent reorder could cause duplicates | Wrap reorder in transaction; clear all hot_orders then reassign |

### Missing Information

- AR-06: confirm 14 as maximum or make configurable (this plan assumes configurable with default 14)

---

## Module 9: Notifications

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth, Listings, Deal Events, Approvals  
**Estimate:** 2–3 days  

### Purpose

Notification creation (event-driven via `BackgroundExecutor`), list, mark read, mark all read, unread count. Notifications are role-scoped.

### Stories Included

- US-001-receive-notification, US-002-mark-read

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| GET | `/notifications` | `list_notifications` |
| GET | `/notifications/unread-count` | `get_unread_count` |
| PATCH | `/notifications/{id}/read` | `mark_read` |
| POST | `/notifications/read-all` | `mark_all_read` |

### Entities Used

- `NotificationEntity`, `UserEntity` (preference filtering)

### Dependencies

- Approvals (notification triggers on approve/reject)
- Deal Events (notification triggers on report/confirm)
- Foundation BackgroundExecutor (async dispatch)

### Files to Create

```
src/data/entities/notification.py          # NotificationEntity — 8 fields
src/data/repositories/notification_repo.py # get_unread_count, mark_all_read, list_by_user
src/data/notifications.py                  # send_notification() helper with preference filtering
src/modules/notifications/__init__.py
src/modules/notifications/router.py        # 4 routes
src/modules/notifications/schemas.py       # Notification, NotificationListResponse
src/modules/notifications/mapper.py        # notification_to_response()
src/modules/notifications/facades/__init__.py
src/modules/notifications/facades/list_notifications.py
src/modules/notifications/facades/get_unread_count.py
src/modules/notifications/facades/mark_read.py
src/modules/notifications/facades/mark_all_read.py
```

**Total: ~12 files**

### Additional Internal File

```
src/data/notifications.py         # Shared helper: send_notification(user_id, event_type, title, body, reference_type, reference_id)
                                   #   - fetches user prefs
                                   #   - skips if event_type disabled
                                   #   - creates NotificationEntity
                                   #   - returns None if skipped
```

### Files to Modify

- `src/main.py` — register `notifications` module
- `src/data/repositories/user_repo.py` — add `get_notification_prefs()` helper
- Facades in listings, deal_events, approvals — add `executor.enqueue(notify_xxx, ...)` on mutation:
  - `create_listing` (submit): `notify_listing_submitted`
  - `approve_item`: `notify_listing_approved` / `notify_deposit_confirmed` / etc.
  - `reject_item`: `notify_listing_rejected` / etc.
  - `report_deposit`: `notify_deposit_reported`
  - `report_closure`: `notify_closure_reported`
  - `report_cancellation`: `notify_cancellation_reported`
  - `report_sold_out`: `notify_sold_out_reported`
  - Expire job (Foundation scheduler): `notify_listing_expired`

### Database Changes

- Add `notifications` table migration (FK → users, composite index: user_id, is_read, created_at DESC)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 8 | List: scoped to current user, read/unread filter, pagination, role-scoping (agent sees own, admin sees all); Unread count: correct after read; Mark read: own notification works, another user's → 404; Mark all read: updates count, returns number updated |
| Integration | 6 | Event triggers notification → appears in list → click navigates to correct listing; mark read → unread count decrements; mark all read → all flagged; preference disabled → notification not created |
| Security | 3 | Agent sees only own notifications; admin sees all; cannot mark another user's notification as read |

### Notification Dispatch Registration

Each facade that triggers a notification calls:

```python
executor.enqueue(notify_listing_approved, listing_id=listing.id)
```

The notification functions are registered in `data/notifications.py` and called by the background worker:

```python
async def notify_listing_approved(listing_id: UUID):
    listing = await listing_repo.get(listing_id)
    await send_notification(
        user_id=listing.created_by_id,
        event_type="listing_approved",
        title=f"{listing.transaction_type} {actor_name} đã duyệt {listing.code}",
        reference_type="LISTING",
        reference_id=listing_id,
    )
```

### Freeze Criteria

- Notifications created on all 15 trigger events
- Agent sees only own-scoped notifications
- Admin sees all notifications
- Mark read / mark all read work correctly
- Unread count badge logic verified

### Risks

| Risk | Mitigation |
|------|------------|
| Async dispatch → events may be lost if worker crashes | Retry 3x on failure, then log and discard (acceptable for v1); persistent queue in v2 |
| Injecting `executor.enqueue()` in 15+ facade methods is invasive | Use after-commit hook pattern or decorator `@notify(...)` |
| Approver notification scope undefined (AR-07) | Assume Approvers see notifications for all queues they can act on (same as Agents: their own activity + all pending items they can approve) |

### Missing Information

- AR-07: Confirm Approver notification scope (assumption above)

---

## Module 10: User Settings

**Status:** ✅ Completed & Frozen  
**Dependencies:** Auth  
**Estimate:** 0.5 days  

### Purpose

Get/update notification preferences stored as JSONB on the User entity. Notification filtering is enforced in the notification dispatch layer.

### Stories Included

- US-003-notification-preferences

### APIs Included

| Method | Path | Facade |
|--------|------|--------|
| GET | `/users/me/notification-preferences` | `get_notification_preferences` |
| PUT | `/users/me/notification-preferences` | `update_notification_preferences` |

### Entities Used

- `UserEntity` (notification_prefs JSONB field)

### Dependencies

- Auth (get_current_user)

### Files to Create

```
src/modules/user_settings/__init__.py
src/modules/user_settings/router.py         # 2 routes
src/modules/user_settings/schemas.py         # NotificationPreferences schema (8 boolean fields)
src/modules/user_settings/mapper.py          # prefs_to_response() — trivially maps dict → Pydantic
src/modules/user_settings/facades/__init__.py
src/modules/user_settings/facades/get_notification_preferences.py
src/modules/user_settings/facades/update_notification_preferences.py
```

**Total: ~7 files**

### Files to Modify

- `src/main.py` — register `user_settings` module
- `src/data/entities/user.py` — ensure `notification_prefs` JSONB field exists (nullable, default None)

### Tests Required

| Type | Count | Scope |
|------|-------|-------|
| Unit | 4 | Get: default prefs returned when null; Update: partial update merges, full update replaces, unknown fields ignored |
| Integration | 2 | Update → GET returns new prefs; invalid data type → 400 |
| API | 4 | GET + PUT + 401 + 400 |

### Risks

| Risk | Mitigation |
|------|------------|
| JSONB schema may drift as new notification event types are added | Use Pydantic `NotificationPreferences` model for both validation and defaults; store as `dict` |
| User creates notification_prefs but notification dispatch should work even if null | `send_notification()` falls back to `DEFAULT_PREFS` (all true) when `notification_prefs` is null |

### Missing Information

- Default preferences: all enabled (true) — confirmed by openapi.yaml schemas default: true

---

## Deferred Modules (Out of Scope v1)

| Module | Entity | Reason | Trigger |
|--------|--------|--------|---------|
| **Reviews** | ReviewEntity, ReviewImageEntity | Business rules undefined (MR-01): who can write, moderation, rating semantics | Requires product decision |
| **Organizations** | OrganizationEntity | AR-13: role display suggests org/team concept not yet modelled | Requires product decision |
| **Audit Log** | — | MR-08: no explicit requirement for consolidated history view | Add if users request |
| **Forgot Password** | — | AR-09: admin reset only for v1 | Add password reset in v2 |
| **Data Export** | — | MR-12: no requirement | Add CSV export in v2 |

---

## Dependency Graph

```
                    ┌──────────────────────────────┐
                    │         Foundation            │
                    │  (config, DI, DB, auth infra, │
                    │   errors, pagination, utils)  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │            Auth              │
                    │  (login, logout, get_current) │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │           Users              │
                    │  (CRUD, deactivate, role)    │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │          Listings            │
                    │  (CRUD, browse, submit,      │
                    │   withdraw, search, filter)  │
                    └──┬────────────┬──────────────┘
                       │            │
            ┌──────────▼──┐  ┌──────▼───────────┐
            │ListingImages│  │   Deal Events    │
            │(upload,     │  │(deposit, closure,│
            │ delete,     │  │ cancellation,    │
            │ reorder,    │  │ sold-out)        │
            │ primary)    │  └──────┬───────────┘
            └─────────────┘         │
                                    │
                         ┌──────────▼───────────┐
                         │      Approvals        │
                         │ (queues, approve,     │
                         │  reject, bulk)        │
                         └──────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
   ┌────────▼────────┐  ┌──────────▼──────────┐  ┌─────────▼──────────┐
   │      Pins       │  │   Hot Products      │  │   Notifications    │
   │(pin, unpin,     │  │(promote, unpromote, │  │(list, mark read,   │
   │ list my pins)   │  │ list, reorder)      │  │ mark all, count)   │
   └─────────────────┘  └─────────────────────┘  └────────────────────┘
                                                         │
                                               ┌─────────▼──────────┐
                                               │   User Settings    │
                                               │(notif prefs get/   │
                                               │ update)            │
                                               └────────────────────┘
```

---

## Recommended Implementation Order

| Order | Module | Rationale |
|-------|--------|-----------|
| 0 | **Foundation** | Everything depends on it |
| 1 | **Auth** | All other modules need authenticated user |
| 2 | **Users** | Auth needs UserRepo; Users depends on Auth for guards |
| 3 | **Listings** | Core domain entity; needed by Images, Deal Events, Approvals, Pins, Hot Products |
| 4 | **Listing Images** | Images needed before listing can be submitted |
| 5 | **Deal Events** | Depends on Listings; needed by Approvals |
| 6 | **Approvals** | Most complex business logic; depends on Deal Events + Listings |
| 7 | **Pins** | Simple, depends only on Listings |
| 8 | **Hot Products** | Simple, depends only on Listings |
| 9 | **Notifications** | Depends on all event-producing modules for dispatch wiring |
| 10 | **User Settings** | Depends only on Auth; can be done anytime after Auth |

### Parallelization Opportunities

| Batch | Modules | Reason |
|-------|---------|--------|
| Batch A | Pins + Hot Products + User Settings | All depend only on Auth + Listings; no cross-dependency |
| Batch B | Listing Images + Deal Events | Both depend only on Listings |

---

## Freeze Checkpoints

| Checkpoint | When | Acceptance Criteria |
|------------|------|---------------------|
| **F-1: Foundation Frozen** | After Foundation module | All platform tests pass, DB migration runs clean, DI container resolves all deps, `create_app()` returns FastAPI instance |
| **F-2: Auth Frozen** | After Auth module | Login/logout/me work, JWT validated, unauthorized routes return 401, deactivated login blocked |
| **F-3: Users Frozen** | After Users module | All 7 user endpoints work, last-admin invariant holds, deactivated login blocked, search/pagination work |
| **F-4: Listings Frozen** | After Listings + Images modules | Full lifecycle works (create→submit→approve→edit→withdraw→delete), search returns correct results, re-approval triggers, admin auto-approves |
| **F-5: Deal Ops Frozen** | After Deal Events module | All 4 event types work, status validation enforced, duplicate deposit blocked, immutable events verified |
| **F-6: Approvals Frozen** | After Approvals module | All 15 queues functional, approve/reject changes status correctly, bulk approve works, concurrent double-approve guard works |
| **F-7: Notifications Frozen** | After Notifications module | Events create notifications, role-scoping correct, mark read/mark all work |
| **F-8: Complete** | All modules done | All 45 endpoints match openapi.yaml, all BDD scenarios pass, ~250 API tests pass |

---

## Open Questions & Blockers

> **All resolved on 2026-06-18.**

| ID | Question | Decision | Affects |
|----|----------|----------|---------|
| **B-01** | Image storage backend | **Local FS** — `UPLOAD_DIR` config value | Module 4 |
| **B-02** | Deposit status change | **Confirmed** — no immediate change, stays CON_HANG until approver | Module 5 |
| **B-03** | `viewCount` increment | **Separate endpoint** `POST /listings/{id}/views` | Module 3 |
| **B-04** | Password on user create | **Admin types it** (field in CreateUserRequest) | Module 2 |
| **B-05** | Approver notification scope | **Same as Admin** — approves see all | Module 9 |
| **B-06** | Re-approval trigger fields | **Price, area fields, image changes** trigger re-approval; **description does not** | Module 3 |
| **B-07** | `transactionType` immutable after submission | **Yes** — only editable in DRAFT | Module 3 |
| **B-08** | `EXPIRATION_DAYS` default | **30**, configurable via env | Foundation |

---

## Module Inventory (Summary)

| Module | Endpoints | Facades | Entity | Stories | Test Count (est.) | Days |
|--------|-----------|---------|--------|---------|-------------------|------|
| Foundation | — | — | 8 tables | — | ~15 | 3–4 |
| Auth | 3 | 3 | User | FL-001 | ~12 | 1–2 |
| Users | 8 | 7 | User | 4 | ~26 | 2–3 |
| Listings | 7 | 7 | Listing, ListingImage | 7 | ~42 | 4–5 |
| Listing Images | 4 | 4 | ListingImage | — | ~15 | 1–2 |
| Deal Events | 4 | 4 | DealEvent | 4 | ~24 | 2–3 |
| Approvals | 6 | 6 | Approval | 5 | ~36 | 4–5 |
| Pins | 3 | 3 | UserPin | 1 | ~14 | 1 |
| Hot Products | 4 | 4 | Listing | 2 | ~14 | 1–2 |
| Notifications | 4 | 4 | Notification | 2 | ~17 | 2–3 |
| User Settings | 2 | 2 | User (JSONB) | 1 | ~10 | 0.5 |
| **Total** | **45** | **45** | **8 entities** | **26 stories** | **~225 tests** | **22–30 days** |

---

*End of Backend Implementation Plan — Biglands v1.0*
