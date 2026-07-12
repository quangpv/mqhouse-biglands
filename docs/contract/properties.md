# Properties

Prefix: `/properties`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix and state machine diagram.

---

## Global Rules

### Draft Visibility
- Draft properties are only visible to their owner
- List endpoint filters out other users' drafts at the query level
- Detail endpoint returns 403 "Draft properties are only visible to their owner" for other users' drafts

### SALE Transaction/Property Type Guard
- On create and update: if user is SALE, `transaction_type_id` must be in the user's assigned `transaction_types`, and `property_type_id` must be in the user's assigned `property_types`
- Returns 403 if mismatch

### Phone Masking
- For SALE users viewing properties they did NOT create: `creator.phone` and `owner_phone` are masked (first 4 digits + `****`)
- ADMIN/APPROVER and property owners always see full numbers

### Code Generation
- Format: `YYMMDD` + 7-digit zero-padded random = 14 characters

### Price Per M2
- Computed as `price / total_area`, quantized to 2 decimal places
- Returns null if either value is missing or zero

---

## POST /properties

Desc: Create property.

**Access:** Authenticated

**Rules:**
- `is_draft=true` (default): status = DRAFT, no transition, no approval, no notification
- `is_draft=false` + SALE: status = POST_PENDING, creates approval + transition, notifies admins/approvers
- `is_draft=false` + ADMIN/APPROVER: status = AVAILABLE directly, no approval/transition/notification
- SALE transaction/property type guard applies

**Request:** `CreatePropertyRequest`
**Response:** `PropertyResponse`

---

## GET /properties

Desc: List all properties with filters.

**Access:** Authenticated

**Rules:**
- Draft properties from other users are filtered out
- Each property includes `is_pinned` flag for the current user
- Phone masking applies for SALE users

**Query Params:** `PropertyListParams`
**Response:** `PropertyListResponse`

---

## GET /properties/counts

Desc: Get property counts by category.

**Access:** Authenticated

**Rules:**
- Returns three counts: `all_count`, `hot_count`, `pinned_count`
- All counts respect the same filters as listing
- `pinned_count` is per-user
- Draft visibility filtering applies

**Response:** `PropertyCountResponse`

---

## GET /properties/{property_id}

Desc: Get property detail.

**Access:** Authenticated

**Rules:**
- Draft properties: returns 403 if viewer is not the owner
- Includes `is_pinned` flag
- Phone masking applies

**Response:** `PropertyResponse`

---

## PUT /properties/{property_id}

Desc: Update property.

**Access:** Authenticated

**Rules:**

| Current Status | Who | Changes Applied? | New Status | Approval Needed? | Notifications |
|---|---|---|---|---|---|
| DRAFT | Owner | Yes, immediately | DRAFT | No | None |
| POST_PENDING | Owner (SALE) | Yes, immediately | POST_PENDING | No | None |
| POST_PENDING | Admin/Approver | Yes, immediately | POST_PENDING | No | Owner notified (LISTING_UPDATED) |
| AVAILABLE | SALE | No (deferred) | EDIT_PENDING | Yes (new) | Admins/approvers notified |
| AVAILABLE | Admin/Approver | Yes, immediately | AVAILABLE | No | None |
| EDIT_PENDING | Owner (SALE) | No (overwrites approval diff) | EDIT_PENDING | Overwrites existing | None |
| EDIT_PENDING | Non-owner Admin/Approver | No (overwrites approval diff) | EDIT_PENDING | Overwrites existing | Owner notified (LISTING_UPDATED) |

**Conflict rules (409):**
- SALE editing AVAILABLE: if pending approval exists → 409
- Editing EDIT_PENDING: if no pending approval exists → 409

**Other rules:**
- SALE can only update own properties
- Allowed statuses: DRAFT, POST_PENDING, AVAILABLE, EDIT_PENDING
- Tag handling: `null` = unchanged, `[]` = clear, `[...]` = replace
- Change snapshot computed for each changed field

**Request:** `UpdatePropertyRequest`
**Response:** `PropertyResponse`

---

## DELETE /properties/{property_id}

Desc: Delete property.

**Access:** Authenticated

**Rules:**
- ADMIN can delete any property
- Non-admin can only delete own properties
- Hard delete for non-terminal statuses (draft, post_pending, available, edit_pending)
- Soft delete for terminal statuses (deposited, soldout, expired, completed)

**Response:** 204 No Content

---

## POST /properties/{property_id}/transitions/submit

Desc: Submit draft for approval/posting.

**Access:** Authenticated (owner only)

**Rules:**
- Status must be DRAFT (403 otherwise)
- SALE: status → POST_PENDING, creates approval, notifies admins/approvers
- ADMIN/APPROVER: status → AVAILABLE directly, no approval/notification

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/withdraw

Desc: Withdraw pending request.

**Access:** SALE only

**Rules:**
- Only SALE can withdraw (403 for ADMIN/APPROVER)
- Only the original requester can withdraw (403 otherwise)

| From Status | Returns To |
|---|---|
| POST_PENDING | DRAFT |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | from_property_status (from approval entity) |

- Existing pending approval is marked REJECTED

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/deposit

Desc: Report deposit or confirm deposit.

**Access:** Authenticated

**Rules:**
- Status must be AVAILABLE (403 otherwise)
- `contract_date` must be >= today (403 "Contract date must be today or later")
- Max 10 files (403 otherwise)
- `customer_name` and `customer_phone` required (422 if missing)
- SALE: status → DEPOSIT_PENDING + approval + notification
- ADMIN/APPROVER: status → DEPOSITED directly

**Request:** `DepositRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/soldout

Desc: Report sold out or confirm sold out.

**Access:** Authenticated

**Rules:**
- Status must be AVAILABLE or DEPOSITED (403 otherwise)
- SALE: status → SOLDOUT_PENDING + approval + notification
- ADMIN/APPROVER: status → SOLDOUT directly

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/cancel

Desc: Cancel deposit or confirm cancellation.

**Access:** Authenticated

**Rules:**
- Status must be DEPOSITED (403 otherwise)
- SALE: status → CANCEL_PENDING + approval + notification
- ADMIN/APPROVER: status → AVAILABLE directly

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/complete

Desc: Complete sale or confirm completion.

**Access:** Authenticated

**Rules:**
- Status must be DEPOSITED (403 otherwise)
- `contract_date` must be >= today (403 otherwise)
- Max 10 files (403 otherwise)
- `customer_name` and `customer_phone` required (422 if missing)
- SALE: status → COMPLETE_PENDING + approval + notification
- ADMIN/APPROVER: status → COMPLETED directly

**Request:** `CompleteRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/reopen

Desc: Reopen a completed/soldout/expired property.

**Access:** Authenticated

**Rules:**
- Only reopenable from SOLDOUT, EXPIRED, or COMPLETED (403 otherwise)
- SALE: must be owner, status → REOPEN_PENDING + approval + notification
- ADMIN/APPROVER: status → AVAILABLE directly; if not owner, notifies owner (REOPEN_APPROVED)

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## GET /properties/{property_id}/status-logs

Desc: Get property status change history.

**Access:** Authenticated

**Rules:**
- Returns paginated transitions ordered by most recent first
- 404 if property not found

**Query Params:** `page` (default 1), `size` (default 20, max 100)
**Response:** `PropertyTransitionListResponse`

---

## GET /properties/{property_id}/status-logs/{log_id}

Desc: Get single status log entry.

**Access:** Authenticated

**Rules:**
- 404 if property or transition not found
- Includes associated files with URLs

**Response:** `PropertyTransitionResponse`

---

## GET /properties/{property_id}/pending-approval

Desc: Get pending approval for a property.

**Access:** Authenticated

**Rules:**
- 404 if property not found
- 404 if no pending approval exists
- Resolves file URLs from `changed_fields.image_ids` if present

**Response:** `ApprovalResponse`

---

## Related

- [Approvals](./approvals.md) — approval workflow, approve/reject decisions
- [Files](./files.md) — file upload for transitions
- [Assets](./assets.md) — pins, hot properties, my assets
- [Notifications](./notifications.md) — state change notifications
