# Assets

Pins, Hot Properties, My Assets, Carts.

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Pins

### POST /properties/{property_id}/pins

Desc: Pin a property.

**Access:** Authenticated

**Rules:**
- 404 if property not found
- 409 "Property already pinned" if already pinned (NOT a toggle)
- One pin per user per property (DB composite PK)

**Response:** `MessageResponse` (201)

### DELETE /properties/{property_id}/pins

Desc: Unpin a property.

**Access:** Authenticated

**Rules:**
- 404 "Property not pinned" if not pinned (NOT a no-op)

**Response:** 204 No Content

### GET /me/pins

Desc: List my pinned properties.

**Access:** Authenticated

**Rules:**
- Returns only the current user's pins
- All returned properties have `is_pinned=true`
- Supports same filters as property list

**Response:** `PropertyListResponse`

---

## Hot Properties

### GET /properties/hots

Desc: List hot properties.

**Access:** Authenticated

**Rules:**
- Returns properties with `is_hot=true`
- Includes `is_pinned` flag per user
- Includes `hot_order` for ordering
- Supports same filters as property list

**Response:** `PropertyListResponse`

### POST /properties/{property_id}/hots

Desc: Promote property to hot.

**Access:** ADMIN only

**Rules:**
- 404 if property not found
- 409 if property already hot
- 409 if property has pending approvals
- Sets `is_hot=true` and `hot_order=max+1` on property

**Request:** `PromoteToHotRequest`
**Response:** `HotPropertyResponse` (201)

### DELETE /properties/{property_id}/hots

Desc: Remove property from hot.

**Access:** ADMIN only

**Rules:**
- 404 if property is not hot
- Clears `is_hot=false` and `hot_order=null` on property

**Response:** 204 No Content

---

## Carts (Property Counts)

### GET /carts/counts

Desc: Count user's properties by status category.

**Access:** Authenticated

**Rules:**
- All counts scoped to `created_by_id=current_user.id`
- Default categories (when no `statuses` param): all, pinned, hot, rejected, + all pending statuses + available, deposited, completed, soldout, expired
- If `statuses` param provided, only returns requested categories
- Special categories: `all` (total), `pinned`, `hot`, `rejected`

**Response:** `CartCountResponse` (dict of category → count)

---

## Expirations (Background Job)

Not an HTTP endpoint — runs as scheduled task.

**Rules:**
- Processes properties with status `DEPOSITED` or `DEPOSIT_PENDING` where `contract_date < today`
- **DEPOSITED properties:** status → EXPIRED, transition created, notifications sent to owner + admins/approvers
- **DEPOSIT_PENDING properties:** rolls back to `from_property_status` (typically AVAILABLE), approval marked REJECTED, DEPOSIT_REJECTED notification to owner only
- Properties with `contract_date == today` are NOT expired (strict `<` comparison)

---

## Related

- [Properties](./properties.md) — property details, status changes
- [Notifications](./notifications.md) — expiration triggers notifications
- [Auth](./auth.md) — my properties, my pins
