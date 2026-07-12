# Approvals

Prefix: `/approvals`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Only Admins and Approvers can manage approvals.
- Approvals track pending requests from Sales staff (or admin edits that require approval).
- Each approval records the property status before the request and the expected status after approval.
- Approval requests can be: pending, approved, or rejected.

---

## GET /approvals

Desc: View pending approval requests.

**Access:** Admin or Approver

**Rules:**
- Returns a paginated list of approval requests.
- Can filter by status, transaction type, property type, district, and price/area range.
- Each item includes a summary of the property and the request details.

**Query Params:** `ApprovalListParams`
**Response:** `ApprovalListResponse`

---

## GET /approvals/counts

Desc: Get approval counts by transaction type and action.

**Access:** Admin or Approver

**Rules:**
- Only counts pending approval requests.
- Groups results by transaction type and action type.
- Returns an empty list if there are no pending approvals.

**Response:** `[ApprovalCountItem]`

---

## GET /approvals/{approval_id}

Desc: View approval request details.

**Access:** Admin or Approver

**Rules:**
- Returns full property details, request details (including changed fields for edit requests), and decision information.
- Resolves file URLs from any image IDs in the change details.
- Invalid image IDs are silently skipped.

**Response:** `ApprovalResponse`

---

## POST /approvals/{approval_id}/approve

Desc: Approve a pending request.

**Access:** Admin or Approver

**Rules:**
- Only pending requests can be approved (otherwise the request is rejected).
- For edit requests: applies all requested changes to the property (including tag and image updates).
- Sets the property status to the expected status recorded in the approval.
- Records a status change in the property's history.
- Sends a notification to the person who made the original request.

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

| Property Status | Notification |
|---|---|
| POST_PENDING | Listing published |
| EDIT_PENDING | Listing edit approved |
| DEPOSIT_PENDING | Deposit confirmed |
| SOLDOUT_PENDING | Sold-out confirmed |
| CANCEL_PENDING | Cancellation confirmed |
| COMPLETE_PENDING | Sale completed |
| REOPEN_PENDING | Reopen approved |

**Request:** `ApprovalDecisionRequest`
**Response:** 204 No Content

---

## POST /approvals/{approval_id}/reject

Desc: Reject a pending request.

**Access:** Admin or Approver

**Rules:**
- Only pending requests can be rejected (otherwise the request is rejected).
- No changes are applied to the property (unlike approve).
- The property reverts to the status it had before the request was made.
- Records a status change in the property's history.
- Sends a notification to the person who made the original request.

**Approval → Property Status mapping:**

| Current Status | Reject → Target |
|---|---|
| POST_PENDING | DRAFT |
| EDIT_PENDING | AVAILABLE |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | Status before the original request |

**Notification events on reject:**

| Property Status | Notification |
|---|---|
| POST_PENDING | Listing rejected |
| EDIT_PENDING | Listing edit rejected |
| DEPOSIT_PENDING | Deposit rejected |
| SOLDOUT_PENDING | Sold-out rejected |
| CANCEL_PENDING | Cancellation rejected |
| COMPLETE_PENDING | Sale completion rejected |
| REOPEN_PENDING | Reopen rejected |

**Request:** `ApprovalDecisionRequest`
**Response:** 204 No Content

---

## Related

- [Properties](./properties.md) — property status changes, history
- [Notifications](./notifications.md) — approval notification events
