# Properties

Prefix: `/properties`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix and state machine diagram.

---

## Global Rules

### Draft Visibility
- Draft properties are only visible to the person who created them.
- When listing properties, other users' drafts are automatically hidden.
- When viewing a specific property that is a draft created by someone else, access is denied.

### Sales Staff Type Guard
- When creating or updating a property, Sales staff can only choose from the property types and transaction types they are assigned to.
- If the selected types are not in the staff member's assignments, the request is denied.

### Phone Number Privacy
- Sales staff see masked phone numbers (first 4 digits + `****`) for properties they did not create.
- Admins, approvers, and property owners always see full phone numbers.

### Property Code
- Each property is assigned a unique 14-character code: date prefix (YYMMDD) + 7-digit random number.

### Price Per Square Meter
- Automatically calculated as price divided by total area, rounded to 2 decimal places.
- Returns empty if either value is missing or zero.

### Auto-Rejection Cascade
- When any user acts on a property that already has a pending approval, the existing approval is automatically rejected.
- This applies to all status transitions (deposit, sold out, cancel, complete, reopen) and edits.
- The auto-rejected approval is recorded as rejected in the approval history.

### First Image as Primary
- When creating or updating a property, the first image in the list is automatically set as the primary image.

### Terminal Statuses
- DEPOSITED, SOLDOUT, EXPIRED, and COMPLETED are terminal statuses.
- Terminal statuses can only be soft-deleted (moved to trash), not hard-deleted.
- The only way out of a terminal status is through the reopen flow.

---

## POST /properties

Desc: Create a property listing.

**Access:** Requires sign-in

**Rules:**
- Saving as draft (`is_draft=true`, default): listing is saved privately; no approval needed; no one is notified.
- Publishing immediately (`is_draft=false`) by Sales staff: listing goes to approval queue; admins and approvers are notified.
- Publishing immediately (`is_draft=false`) by Admin/Approver: listing is published right away; no approval needed; no one is notified.
- Sales staff type guard applies (see Global Rules).

**Required fields for publish:**
- Title: minimum 1 character.
- Description: minimum 30 characters.
- At least 1 image is required.
- Property type and transaction type must be selected.

**Draft vs. Publish:**
- Saving as draft only requires a subset of fields (title, types, location, price, phone, description). Images are not required for drafts.
- Once a draft is published, it cannot be re-published. Only save changes is available.

**Request:** `CreatePropertyRequest`
**Response:** `PropertyResponse`

---

## GET /properties

Desc: View all property listings with filters.

**Access:** Requires sign-in

**Rules:**
- Draft properties created by other users are automatically hidden.
- Each property indicates whether you have pinned it.
- Phone number masking applies for Sales staff viewing properties they did not create.

**Query Params:** `PropertyListParams`
**Response:** `PropertyListResponse`

---

## GET /properties/counts

Desc: Get property counts by category.

**Access:** Requires sign-in

**Rules:**
- Returns three counts: total, hot (featured), and pinned.
- All counts respect the same filters as property listing.
- Pinned count is per-user (each user sees how many properties they have pinned).
- Draft visibility filtering applies.

**Response:** `PropertyCountResponse`

---

## GET /properties/{property_id}

Desc: View property details.

**Access:** Requires sign-in

**Rules:**
- Draft properties: access is denied if you are not the person who created the listing.
- Indicates whether you have pinned this property.
- Phone number masking applies for Sales staff viewing properties they did not create.

**Response:** `PropertyResponse`

---

## PUT /properties/{property_id}

Desc: Update a property listing.

**Access:** Requires sign-in

**Rules:**

| Current Status | Who | Changes Applied? | New Status | Approval Needed? | Notifications |
|---|---|---|---|---|---|
| DRAFT | Owner | Yes, immediately | DRAFT | No | None |
| POST_PENDING | Owner (Sales) | Yes, immediately | POST_PENDING | No | None |
| POST_PENDING | Admin/Approver | Yes, immediately | POST_PENDING | No | Owner notified (listing updated) |
| AVAILABLE | Sales | No (deferred) | EDIT_PENDING | Yes (new) | Admins/approvers notified |
| AVAILABLE | Admin/Approver | Yes, immediately | AVAILABLE | No | None |
| EDIT_PENDING | Owner (Sales) | No (overwrites approval diff) | EDIT_PENDING | Overwrites existing | None |
| EDIT_PENDING | Non-owner Admin/Approver | No (overwrites approval diff) | EDIT_PENDING | Overwrites existing | Owner notified (listing updated) |

**Conflict rules:**
- Sales staff editing an AVAILABLE listing: if there is already a pending edit request, the update is rejected.
- Editing an EDIT_PENDING listing: if there is no pending approval record, the update is rejected.

**Other rules:**
- Sales staff can only update their own properties.
- Only listings in the following statuses can be edited: DRAFT, POST_PENDING, AVAILABLE, EDIT_PENDING.
- Tag handling: `null` = leave unchanged, `[]` = clear all tags, `[...]` = replace with new set.
- A snapshot of changes is recorded for each modified field.

**Request:** `UpdatePropertyRequest`
**Response:** `PropertyResponse`

---

## DELETE /properties/{property_id}

Desc: Delete a property listing.

**Access:** Requires sign-in

**Rules:**
- Admins can delete any property.
- Non-admins can only delete their own properties.
- Listings that are not yet finalized (draft, pending posting, available, pending edit) are permanently deleted.
- Listings that have reached a final status (deposited, sold out, expired, completed) are soft-deleted (moved to trash).

**Response:** 204 No Content

---

## POST /properties/{property_id}/transitions/submit

Desc: Submit a draft listing for publication.

**Access:** Requires sign-in (owner only)

**Rules:**
- Listing must be in DRAFT status.
- Sales staff: listing goes to approval queue; admins and approvers are notified.
- Admin/Approver: listing is published immediately; no approval needed; no one is notified.

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/withdraw

Desc: Withdraw a pending request.

**Access:** Sales staff only

**Rules:**
- Only Sales staff can withdraw (Admins and Approvers cannot use this action).
- Only the person who originally submitted the request can withdraw it.

| From Status | Returns To |
|---|---|
| POST_PENDING | DRAFT |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | Status before the original request |

- The existing pending approval is marked as rejected.

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/deposit

Desc: Report a deposit or confirm a deposit.

**Access:** Requires sign-in

**Rules:**
- Listing must be in AVAILABLE status.
- Contract date must be today or later.
- Maximum of 10 supporting files allowed (including deposit images and certificate images).
- Customer name and customer phone are required.
- Sales staff: deposit goes to approval queue; admins and approvers are notified.
- Admin/Approver: deposit is confirmed immediately; no approval needed.

**Request:** `DepositRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/soldout

Desc: Report a listing as sold out or confirm it is sold out.

**Access:** Requires sign-in

**Rules:**
- Listing must be in AVAILABLE or DEPOSITED status.
- Sales staff: sold-out request goes to approval queue; admins and approvers are notified.
- Admin/Approver: listing is marked as sold out immediately; no approval needed.

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/cancel

Desc: Cancel a deposit or confirm cancellation.

**Access:** Requires sign-in

**Rules:**
- Listing must be in DEPOSITED status.
- Sales staff: cancellation goes to approval queue; admins and approvers are notified.
- Admin/Approver: listing is returned to AVAILABLE immediately; no approval needed.

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/complete

Desc: Complete a sale or confirm completion.

**Access:** Requires sign-in

**Rules:**
- Listing must be in DEPOSITED status.
- Contract date must be today or later.
- Maximum of 10 supporting files allowed (including completion images and certificate images).
- Customer name and customer phone are required.
- Sales staff: completion goes to approval queue; admins and approvers are notified.
- Admin/Approver: listing is marked as completed immediately; no approval needed.

**Request:** `CompleteRequest`
**Response:** `PropertyResponse`

---

## POST /properties/{property_id}/transitions/reopen

Desc: Reopen a completed, sold-out, or expired listing.

**Access:** Requires sign-in

**Rules:**
- Can only reopen from SOLDOUT, EXPIRED, or COMPLETED status.
- Sales staff: must be the owner of the listing; reopen goes to approval queue; admins and approvers are notified.
- Admin/Approver: listing is reopened immediately; if not the owner, the owner is notified.

**Request:** `NotesRequest`
**Response:** `PropertyResponse`

---

## GET /properties/{property_id}/status-logs

Desc: View the status change history of a property.

**Access:** Requires sign-in

**Rules:**
- Returns a paginated list of all status changes, most recent first.
- Returns an error if the property is not found.

**Query Params:** `page` (default 1), `size` (default 20, max 100)
**Response:** `PropertyTransitionListResponse`

---

## GET /properties/{property_id}/status-logs/{log_id}

Desc: View a single status log entry.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the property or the log entry is not found.
- Includes any associated files with their URLs.

**Response:** `PropertyTransitionResponse`

---

## GET /properties/{property_id}/pending-approval

Desc: View the pending approval request for a property.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the property is not found or if there is no pending approval.
- Resolves file URLs from any image IDs in the change details.

**Response:** `ApprovalResponse`

---

## Related

- [Approvals](./approvals.md) — approval workflow, approve/reject decisions
- [Files](./files.md) — file upload for transitions
- [Assets](./assets.md) — pins, hot properties, my assets
- [Notifications](./notifications.md) — state change notifications
