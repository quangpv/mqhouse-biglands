# Notifications

Prefix: `/notifications`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Each user sees only their own notifications.
- Notifications are created automatically when property status changes.
- Real-time delivery via WebSocket.
- 23 notification types covering all property workflow events.

---

## Notification Events

### Property State Change Notifications

| Event | Trigger | Recipients |
|---|---|---|
| LISTING_POST_CREATED | Sales staff creates/submits a property | Admins + Approvers (type-scoped) |
| LISTING_POST_APPROVED | Admin/Approver approves a listing request | Property owner |
| LISTING_POST_REJECTED | Admin/Approver rejects a listing request | Property owner |
| EDITING_POST_APPROVED | Admin/Approver approves an edit | Property owner |
| EDIT_REJECTED | Admin/Approver rejects an edit | Property owner |
| DEPOSIT_REPORTED | Sales staff reports a deposit | Admins + Approvers (type-scoped) |
| DEPOSIT_CONFIRMED | Admin/Approver confirms a deposit | Property owner |
| DEPOSIT_REJECTED | Admin/Approver rejects a deposit | Property owner |
| SOLDOUT_REPORTED | Sales staff reports sold-out | Admins + Approvers (type-scoped) |
| SOLDOUT_CONFIRMED | Admin/Approver confirms sold-out | Property owner |
| SOLDOUT_REJECTED | Admin/Approver rejects sold-out | Property owner |
| CANCELLATION_REPORTED | Sales staff reports cancellation | Admins + Approvers (type-scoped) |
| CANCELLATION_CONFIRMED | Admin/Approver confirms cancellation | Property owner |
| CANCELLATION_REJECTED | Admin/Approver rejects cancellation | Property owner |
| CLOSURE_REPORTED | Sales staff reports completion | Admins + Approvers (type-scoped) |
| CLOSURE_CONFIRMED | Admin/Approver confirms completion | Property owner |
| CLOSURE_REJECTED | Admin/Approver rejects completion | Property owner |
| LISTING_UPDATED | Admin/Approver edits a property | Property owner |
| LISTING_EXPIRED | Auto-expiration job runs | Property owner + Admins + Approvers (type-scoped) |
| REOPEN_REQUESTED | Sales staff requests reopen | Admins + Approvers (type-scoped) |
| REOPEN_APPROVED | Admin/Approver approves reopen | Property owner |
| REOPEN_REJECTED | Admin/Approver rejects reopen | Property owner |

### Notification Rules
- `notify_admins_and_approvers`: sends to all active admins (globally) and active approvers whose assigned transaction types AND property types include the property's types (deduplicates by user ID). Soft-deleted users are excluded. Gated by the `is_notify_approver_for_approval` system setting.
- `notify_property_user`: sends to the property owner. If the owner has been soft-deleted, no notification is sent. Gated by the `is_notify_sale_for_approved` system setting.
- Title is auto-formatted using Vietnamese action strings.
- Body text is in Vietnamese, including property codes and dates.
- Actor name is "Hệ thống" (System) for automated actions like expiration.
- A WebSocket event is sent for each notification creation.

---

## GET /notifications

Desc: View your notifications.

**Access:** Requires sign-in

**Rules:**
- Scoped to the current user only.
- Can filter by read/unread status, transaction type, and search text (searches title and body).
- Ordered by most recent first.

**Query Params:** `NotificationListParams`
**Response:** `NotificationListResponse`

---

## GET /notifications/counts

Desc: Get notification counts by category.

**Access:** Requires sign-in

**Rules:**
- Groups notifications by transaction type.
- Can filter by read/unread status and search text.
- Returns the total count across all categories.

**Response:** `NotificationCountResponse`

---

## PATCH /notifications/{id}/read

Desc: Mark a single notification as read.

**Access:** Requires sign-in

**Rules:**
- Only the notification owner can mark it as read.
- Marks the notification as read.

**Response:** `NotificationResponse`

---

## PATCH /notifications/read-all

Desc: Mark all notifications as read.

**Access:** Requires sign-in

**Rules:**
- Marks all unread notifications for the current user as read in a single operation.

**Response:** `MessageResponse`

---

## Related

- [Properties](./properties.md) — state changes trigger notifications
- [Approvals](./approvals.md) — approve/reject triggers notifications
- [System](./system.md) — WebSocket delivers notifications in real-time
