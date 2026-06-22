# Backend Gaps Plan — Biglands

> Backend plan derived from 11 screen `.gap.md` files + frontend plan open questions.
> Purpose: document all gaps between what the UI needs and what `openapi.yaml` currently provides.

## Status: ✅ All items implemented

| Priority | Count | Status |
|---|---|---|
| Must Have (M-01 → M-07) | 7 | ✅ All implemented |
| Should Have (S-01 → S-10) | 10 | ✅ All implemented |
| Could Have (C-01 → C-03) | 3 | ✅ All implemented |

See `.ai/plans/plan1.md` for per-item annotations.

## 1. Organization Entity (Why Needed)

**Source**: SC-009 User Management List gap

**Problem**: `User.role` is enum `AGENT | APPROVER | ADMIN`. But the UI column displays organization/team names like "MQ Land", "ID Land" — not role enum values. These are two distinct concepts:

| Concept | Meaning | Example |
|---|---|---|
| **Role** | System permission level | AGENT = can post listings |
| **Organization** | Company/group the user belongs to | MQ Land, ID Land |

With only `role: AGENT`, the UI **cannot render** "MQ Land". No amount of frontend mapping solves this — the data simply doesn't exist in the API.

**Solution**: Add `Organization` entity

- `Organization`: `{ id: uuid, name: string, displayName: string, createdAt, updatedAt }`
- `User.organizationId`: FK → `Organization` (nullable — an admin might not belong to any org)
- `User.organizationName`: convenience field embedded in User response for list display

**Why entity over `displayRole: string`**:
- Screen shows real org names, not role labels
- Future: filter users by org, reports per org, permissions scoped to org
- `displayRole` is a band-aid that solves nothing beyond display

## 2. Comprehensive Gap Inventory

### Legend

| Priority | Meaning | Count |
|---|---|---|
| **Must** | UI cannot function without this | 7 |
| **Should** | UX degraded or needs workaround | 10 |
| **Could** | Enhancement, nice-to-have | 3 |

### Must Have

| # | Gap | Screens | Fix |
|---|---|---|---|
| **M-01** | `createdBy` filter on `GET /listings` | SC-002, SC-006 | Add `createdBy` query param (UUID or `"me"` shorthand) |
| **M-02** | Multi-status filter on `GET /listings` | SC-006 | Add comma-separated `status=CON_HANG,DA_COC` support |
| **M-03** | `dealEvent` missing from `ApprovalQueueItem` | SC-008 | Add `dealEvent: DealEvent` (nullable) — populated for deposit/closure/cancellation/sold-out queues |
| **M-04** | Organization entity missing | SC-009 | Add `Organization` schema + `organizationId` / `organizationName` on `User` |
| **M-05** | Image validation on submit | SC-004 | Validate ≥1 image when `action=submit` (BR-007) |
| **M-06** | Transaction type lock rule undefined | SC-005 | Document: `transactionType` is **write-once** after first submission (immutable) |
| **M-07** | Review endpoints missing | SC-003 | Add 4 endpoints (see §4) |

### Should Have

| # | Gap | Screens | Fix |
|---|---|---|---|
| **S-01** | `pricePerM2` missing from `Listing` | SC-002, SC-003 | Add `pricePerM2: number` (nullable, computed server-side) |
| **S-02** | `creator` embedded object missing | SC-002, SC-003 | Add `creator: { id, fullName, phone }` to `Listing` response |
| **S-03** | `filterCounts` on `ListingListResponse` | SC-002 | Add `filterCounts: { all: int, hot: int, pinned: int }` |
| **S-04** | View count never increments | SC-003 | Auto-increment on `GET /listings/{id}` or add `POST /listings/{id}/views` |
| **S-05** | `requiresApproval` flag on update | SC-005 | Add `requiresApproval: boolean` to `PUT /listings/{id}` 200 response |
| **S-06** | `reportedBy` + `notes` on `ApprovalQueueItem` | SC-008 | Add `reportedBy: { id, fullName }` and `notes: string` |
| **S-07** | `isHot` filter on `GET /listings` | SC-011 | Add `isHot: boolean` query param |
| **S-08** | `ACCOUNT_DEACTIVATED` error code | SC-001 | Add error code for deactivated account login attempt (USR-I02) |
| **S-09** | Auto-generate password flow | SC-009, SC-010 | Make `password` optional in `CreateUserRequest`; add `generatedPassword: string` to 201 response |
| **S-10** | Notification filters + counts | SC-007 | Add `transactionType` query param + `unreadCount: int` + `categoryCounts` to response |

### Could Have

| # | Gap | Screens | Fix |
|---|---|---|---|
| **C-01** | `q` search on notifications | SC-007 | Add `q` query param to `GET /notifications` |
| **C-02** | Date-range + agent filter on queues | SC-008 | Add `createdAfter`, `createdBefore`, `agentId` params |
| **C-03** | Structured notification fields | SC-007 | Add `eventType`, `actorName`, `transactionType` to `Notification` |

### Already Tracked (OQ cross-reference)

| OQ | Priority | Status |
|---|---|---|
| OQ-01 → **M-01** | Must | Confirmed |
| OQ-02 → **M-07** | Must | Confirmed |
| OQ-03 → **S-10** | Should | Confirmed |
| OQ-04 → **S-02** | Should | Confirmed |
| OQ-05 → **S-01** | Should | Confirmed |
| OQ-06 → **S-09** | Should | Confirmed |
| OQ-07 → **(deferred)** | Deferred | Still no endpoint — defer per discussion |
| OQ-08 → **documentation** | Low | Extract from backend enum; document 15 queueType values |

## 3. Decided Design Decisions

| Question | Decision | Rationale |
|---|---|---|
| Organization vs `displayRole` | **Entity `Organization`** | Real org names, extensible (filter, reports, permissions) |
| Multi-status filter format | **Comma-separated** `?status=CON_HANG,DA_COC` | Simple, standard, no new schema needed |
| Forgot password | **Implement** `POST /auth/forgot-password` + `POST /auth/reset-password` | Required by login screen UI |
| Reviews | **Implement** 4 endpoints | Required by product detail screen UI |
| Transaction type mutability | **Write-once** after first submission | Prevents data integrity bypass; matches screen expectation |

## 4. Specific OpenAPI Changes

### 4.1 New Schemas

```yaml
Organization:
  type: object
  required: [id, name, displayName]
  properties:
    id:
      type: string
      format: uuid
    name:
      type: string
      maxLength: 100
    displayName:
      type: string
      maxLength: 200
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time

Review:
  type: object
  required: [id, listingId, authorId, content, createdAt]
  properties:
    id:
      type: string
      format: uuid
    listingId:
      type: string
      format: uuid
    authorId:
      type: string
      format: uuid
    authorName:
      type: string
    content:
      type: string
      maxLength: 2000
    images:
      type: array
      items:
        type: string
        format: uri
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time
```

### 4.2 Schema Modifications

**`User`** — add:
- `organizationId: string (uuid)` nullable
- `organizationName: string` nullable (convenience)

**`Listing`** — add:
- `pricePerM2: number` nullable
- `creator: object { id, fullName, phone }`

**`ListingListResponse`** — add:
- `filterCounts: { all: int, hot: int, pinned: int }`

**`NotificationListResponse`** — add:
- `unreadCount: int`
- `categoryCounts: { all: int, BAN: int, CHO_THUE: int, SANG_NHUONG: int }`

**`Notification`** — add optional:
- `eventType: string`
- `actorName: string`
- `transactionType: TransactionType`

**`ApprovalQueueItem`** — add:
- `dealEvent: DealEvent` nullable
- `reportedBy: { id: uuid, fullName: string }` nullable
- `notes: string` nullable

**`CreateUserRequest`** — make `password` optional

**`LoginResponse`** / **`ApiError`** — add:
- `ACCOUNT_DEACTIVATED` to error codes

**`PUT /listings/{id}` response** — add:
- `requiresApproval: boolean`

### 4.3 New Endpoints

```
# Reviews
GET    /listings/{listingId}/reviews?page=&size=
POST   /listings/{listingId}/reviews          { content }
DELETE /listings/{listingId}/reviews/{reviewId}
POST   /listings/{listingId}/reviews/{reviewId}/images  (multipart)

# Forgot Password
POST /auth/forgot-password  { email }
POST /auth/reset-password   { token, password }

# View count
POST /listings/{id}/views   (optional — or auto-increment on GET)
```

### 4.4 New Query Parameters

| Endpoint | Param | Type | Description |
|---|---|---|---|
| `GET /listings` | `createdBy` | string (uuid or `"me"`) | Filter by creator |
| `GET /listings` | `status` | string (comma-separated) | Multi-status: `CON_HANG,DA_COC` |
| `GET /listings` | `isHot` | boolean | Filter hot listings |
| `GET /notifications` | `transactionType` | enum | `BAN`, `CHO_THUE`, `SANG_NHUONG` |
| `GET /notifications` | `q` | string | Search in title/body |
| `GET /approvals/queues/{queueType}` | `createdAfter` | date-time | Date range start |
| `GET /approvals/queues/{queueType}` | `createdBefore` | date-time | Date range end |
| `GET /approvals/queues/{queueType}` | `agentId` | uuid | Filter by reporter |

## 5. Implementation Order

| Phase | Items | Effort Estimate |
|---|---|---|
| **Phase 1** (Must) | M-01 through M-07 | High — 7 items including new entity and 6 new endpoints |
| **Phase 2** (Should) | S-01 through S-10 | Medium — mostly field additions + 1 new endpoint |
| **Phase 3** (Could) | C-01 through C-03 | Low — query params + optional fields |
| **Deferred** | Forgot password, OQ-07 | TBD — no backend capacity yet |

## 6. Review Endpoints — Business Rules

### Decided Rules (from brainstorm session)

| Question | Decision | Rationale |
|---|---|---|
| Who can create? | **Any authenticated user** | B2B platform — all users are professional agents. No special precondition. |
| Who can delete? | **Author + Admin** | Author deletes own; Admin moderates any. |
| Moderation? | **Auto-publish** (no pre-moderation) | Professional users; reactive moderation by Admin. Field `isModerated` optional for future. |
| Rating? | **Text-only** | SC-003 screen shows no star/numeric input. Keep `rating: Integer nullable` in schema for future. |
| Max per user per listing? | **1** (409 on duplicate) | Prevents spam. PUT for update can be added later. |
| Images? | **Max 10**, 5MB each, `jpg/png/webp` | Same storage pattern as `ListingImage`. Post-moderation (auto-publish). |

### Request/Response Design

```yaml
CreateReviewRequest:
  type: object
  required: [content]
  properties:
    content:
      type: string
      minLength: 1
      maxLength: 2000

Review:
  type: object
  required: [id, listingId, authorId, authorName, content, createdAt]
  properties:
    id:
      type: string
      format: uuid
    listingId:
      type: string
      format: uuid
    authorId:
      type: string
      format: uuid
    authorName:
      type: string
    content:
      type: string
      maxLength: 2000
    images:
      type: array
      items:
        $ref: "#/components/schemas/ReviewImage"
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time
      nullable: true

ReviewImage:
  type: object
  required: [id, reviewId, url, order]
  properties:
    id:
      type: string
      format: uuid
    reviewId:
      type: string
      format: uuid
    url:
      type: string
      format: uri
    order:
      type: integer
      minimum: 1

ReviewListResponse:
  type: object
  required: [data, pagination]
  properties:
    data:
      type: array
      items:
        $ref: "#/components/schemas/Review"
    pagination:
      $ref: "#/components/schemas/Pagination"
```

### Endpoints

```
GET    /listings/{listingId}/reviews?page=&size=
       → 200 ReviewListResponse
       → 401/403 if not authenticated

POST   /listings/{listingId}/reviews
       Body: { content: string }
       → 201 Review
       → 400 ValidationError
       → 409 Conflict (already reviewed)

DELETE /listings/{listingId}/reviews/{reviewId}
       → 204 No Content
       → 403 Forbidden (not author and not admin)

POST   /listings/{listingId}/reviews/{reviewId}/images
       Multipart: file
       → 201 ReviewImage
       → 400 if exceeds 10 images

GET    /listings/{listingId}/reviews/{reviewId}
       → 200 Review (with images)
       (optional — for edit pre-fill)
```
