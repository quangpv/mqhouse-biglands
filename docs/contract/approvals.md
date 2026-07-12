# Approvals

Prefix: `/approvals`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Only `ADMIN` and `APPROVER` can access approval endpoints
- Approvals track pending requests from SALE users (or admin edits requiring approval)
- Each approval has `from_property_status` (before request) and `to_property_status` (after approval)
- Approval status transitions: `PENDING` → `APPROVED` or `REJECTED`

---

## GET /approvals

Desc: List pending approvals.

**Access:** ADMIN or APPROVER

**Rules:**
- Returns paginated list of approvals
- Supports filtering by status, transaction type, property type, district, price/area range
- Each item includes property summary and request details

**Query Params:** `ApprovalListParams`
**Response:** `ApprovalListResponse`

---

## GET /approvals/counts

Desc: Get approval counts by transaction type and action.

**Access:** ADMIN or APPROVER

**Rules:**
- Counts only PENDING approvals
- Groups by `(transaction_type_id, action)`
- Returns empty list if no pending approvals

**Response:** `[ApprovalCountItem]`

---

## GET /approvals/{approval_id}

Desc: Get approval detail.

**Access:** ADMIN or APPROVER

**Rules:**
- Returns full property, request details (including `changed_fields` for edit approvals), and decision info
- Resolves file URLs from `changed_fields.image_ids`
- Invalid UUIDs in image lists are silently skipped

**Response:** `ApprovalResponse`

---

## POST /approvals/{approval_id}/approve

Desc: Approve a pending request.

**Access:** ADMIN or APPROVER

**Rules:**
- Approval must be PENDING (409 otherwise)
- Applies `changed_fields` to property for edit approvals (tags, images synced)
- Sets property status to `approval.to_property_status`
- Creates transition record with action=APPROVE
- Sends notification to original requester

**Approval → Property Status mapping:**

| Current Status | Approve → Target |
|---|---|
| POST_PENDING | AVAILABLE |
| EDIT_PENDING | AVAILABLE (with field changes applied) |
| DEPOSIT_PENDING | DEPOSITED |
| SOLDOUT_PENDING | SOLDOUT |
| CANCEL_PENDING | AVAILABLE |
| COMPLETE_PENDING | COMPLETED |
| REOPEN_PENDING | AVAILABLE |

**Notification events on approve:**

| Property Status | Event |
|---|---|
| POST_PENDING | LISTING_POST_APPROVED |
| EDIT_PENDING | EDITING_POST_APPROVED |
| DEPOSIT_PENDING | DEPOSIT_CONFIRMED |
| SOLDOUT_PENDING | SOLDOUT_CONFIRMED |
| CANCEL_PENDING | CANCELLATION_CONFIRMED |
| COMPLETE_PENDING | CLOSURE_CONFIRMED |
| REOPEN_PENDING | REOPEN_APPROVED |

**Request:** `ApprovalDecisionRequest`
**Response:** 204 No Content

---

## POST /approvals/{approval_id}/reject

Desc: Reject a pending request.

**Access:** ADMIN or APPROVER

**Rules:**
- Approval must be PENDING (409 otherwise)
- NO changed_fields applied (unlike approve)
- Sets property status to `approval.from_property_status` (rolls back)
- Creates transition record with action=REJECT
- Sends notification to original requester

**Approval → Property Status mapping:**

| Current Status | Reject → Target |
|---|---|
| POST_PENDING | DRAFT |
| EDIT_PENDING | AVAILABLE |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | from_property_status (e.g., SOLDOUT) |

**Notification events on reject:**

| Property Status | Event |
|---|---|
| POST_PENDING | LISTING_POST_REJECTED |
| EDIT_PENDING | EDIT_REJECTED |
| DEPOSIT_PENDING | DEPOSIT_REJECTED |
| SOLDOUT_PENDING | SOLDOUT_REJECTED |
| CANCEL_PENDING | CANCELLATION_REJECTED |
| COMPLETE_PENDING | CLOSURE_REJECTED |
| REOPEN_PENDING | REOPEN_REJECTED |

**Request:** `ApprovalDecisionRequest`
**Response:** 204 No Content

---

## Related

- [Properties](./properties.md) — property state machine, transitions
- [Notifications](./notifications.md) — approval notification events
