# Notifications

Prefix: `/notifications`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Each user sees only their own notifications (scoped by `user_id`)
- Notifications created automatically on property state changes
- Real-time delivery via WebSocket
- 23 notification types covering all property workflow events

---

## Notification Events

### Property State Change Notifications

| Event | Trigger | Recipients |
|---|---|---|
| LISTING_POST_CREATED | SALE creates/submits property | Admins + Approvers |
| LISTING_POST_APPROVED | Admin approves post request | Property owner |
| LISTING_POST_REJECTED | Admin rejects post request | Property owner |
| EDITING_POST_APPROVED | Admin approves edit | Property owner |
| EDIT_REJECTED | Admin rejects edit | Property owner |
| DEPOSIT_REPORTED | SALE reports deposit | Admins + Approvers |
| DEPOSIT_CONFIRMED | Admin confirms deposit | Property owner |
| DEPOSIT_REJECTED | Admin rejects deposit | Property owner |
| SOLDOUT_REPORTED | SALE reports soldout | Admins + Approvers |
| SOLDOUT_CONFIRMED | Admin confirms soldout | Property owner |
| SOLDOUT_REJECTED | Admin rejects soldout | Property owner |
| CANCELLATION_REPORTED | SALE reports cancellation | Admins + Approvers |
| CANCELLATION_CONFIRMED | Admin confirms cancellation | Property owner |
| CANCELLATION_REJECTED | Admin rejects cancellation | Property owner |
| CLOSURE_REPORTED | SALE reports completion | Admins + Approvers |
| CLOSURE_CONFIRMED | Admin confirms completion | Property owner |
| CLOSURE_REJECTED | Admin rejects completion | Property owner |
| LISTING_UPDATED | Admin/approver edits property | Property owner |
| LISTING_EXPIRED | Auto-expiration job | Property owner + Admins + Approvers |
| REOPEN_REQUESTED | SALE requests reopen | Admins + Approvers |
| REOPEN_APPROVED | Admin approves reopen | Property owner |
| REOPEN_REJECTED | Admin rejects reopen | Property owner |

### Notification Rules
- `notify_admins_and_approvers`: sends to all admins + approvers in the property's organization (deduplicates by user ID)
- `notify_property_user`: sends to the property owner
- Title auto-formatted using Vietnamese action strings
- WebSocket event sent for each notification creation

---

## GET /notifications

Desc: List my notifications.

**Access:** Authenticated

**Rules:**
- Scoped to current user only
- Filterable by `is_read`, `transaction_type`, `search` (ILIKE on title/body)
- Ordered by `created_at DESC`

**Query Params:** `NotificationListParams`
**Response:** `NotificationListResponse`

---

## GET /notifications/counts

Desc: Get notification counts by category.

**Access:** Authenticated

**Rules:**
- Groups notifications by `transaction_type`
- Filterable by `is_read` and `search`
- Returns total sum across all categories

**Response:** `NotificationCountResponse`

---

## PATCH /notifications/{id}/read

Desc: Mark single notification as read.

**Access:** Authenticated

**Rules:**
- Only notification owner can mark as read (403 otherwise)
- Sets `is_read=true`

**Response:** `NotificationResponse`

---

## PATCH /notifications/read-all

Desc: Mark all notifications as read.

**Access:** Authenticated

**Rules:**
- Bulk-updates all unread notifications for current user
- Single UPDATE query

**Response:** `MessageResponse`

---

## Related

- [Properties](./properties.md) — state changes trigger notifications
- [Approvals](./approvals.md) — approve/reject triggers notifications
- [System](./system.md) — WebSocket delivers notifications in real-time
