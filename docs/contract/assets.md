# Assets

Pins, Hot Properties, My Assets, Carts.

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Pins

### POST /properties/{property_id}/pins

Desc: Pin a property.

**Access:** Requires sign-in

**Rules:**
- The property must exist in the system.
- A property can only be pinned once per user. If already pinned, the request is rejected.
- One pin per user per property.

**Response:** `MessageResponse` (201)

### DELETE /properties/{property_id}/pins

Desc: Unpin a property.

**Access:** Requires sign-in

**Rules:**
- The property must currently be pinned. If not pinned, the request is rejected (not a no-op).

**Response:** 204 No Content

### GET /me/pins

Desc: View your pinned properties.

**Access:** Requires sign-in

**Rules:**
- Returns only properties you have pinned.
- All returned properties indicate they are pinned.
- Supports the same filters as property listing.

**Response:** `PropertyListResponse`

---

## Hot Properties

### GET /properties/hots

Desc: View hot (featured) properties.

**Access:** Requires sign-in

**Rules:**
- Returns properties that are marked as hot (featured).
- Each property indicates whether you have pinned it.
- Returns the display order for hot properties.
- Supports the same filters as property listing.

**Response:** `PropertyListResponse`

### POST /properties/{property_id}/hots

Desc: Feature a property as hot.

**Access:** Admin only

**Rules:**
- The property must exist in the system.
- The property cannot already be featured as hot.
- The property cannot have any pending approval requests.
- Sets the property as hot and assigns it the next display order position.

**Request:** `PromoteToHotRequest`
**Response:** `HotPropertyResponse` (201)

### DELETE /properties/{property_id}/hots

Desc: Remove a property from hot (featured) status.

**Access:** Admin only

**Rules:**
- The property must currently be hot. If not, the request is rejected.
- Removes the hot status and display order.

---

## Carts (Property Counts)

### GET /carts/counts

Desc: View your property counts by status category.

**Access:** Requires sign-in

**Rules:**
- All counts are scoped to properties you created.
- Default categories (when no `statuses` parameter): total, pinned, hot, rejected, plus all pending statuses and available, deposited, completed, sold out, expired.
- If specific statuses are requested, only those categories are returned.
- Special categories: `total` (all properties), `pinned`, `hot`, `rejected`.

**Response:** `CartCountResponse` (dict of category → count)

---

## Expirations (Background Job)

Not an HTTP endpoint — runs as a scheduled task at **midnight daily**.

**Trigger condition:**
- Processes properties in DEPOSITED or DEPOSIT_PENDING status.
- Uses the **most recent deposit transition's contract date** (not the property itself).
- Expires if the contract date is **strictly before today** (no grace period).
- Properties with a contract date of today are NOT expired.

**DEPOSITED properties:**
- Status changes to EXPIRED.
- The system ("Hệ thống") acts as the actor for the status change.
- Transition notes: "Hết hạn hợp đồng" (Contract expired).
- Notifications sent to: property owner, all admins, and approvers in the same organization.

**DEPOSIT_PENDING properties:**
- The pending deposit approval is **rejected** (not cancelled).
- Status rolls back to the **previous status before the deposit request** (stored on the approval record).
- Transition notes: "Tự động từ chối do hết hạn hợp đồng" (Auto-rejected due to contract expiration).
- Notification sent to: property owner only (no admin/approver notification).

---

## Related

- [Properties](./properties.md) — property details, status changes
- [Notifications](./notifications.md) — expiration triggers notifications
- [Auth](./auth.md) — your properties, your pins
