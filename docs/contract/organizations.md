# Organizations

Prefix: `/organizations`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Viewing organizations is available to all signed-in users.
- Creating, updating, and deleting organizations require Admin role.
- Updates require all fields to be provided (full replace, not partial update).
- Organization names must be unique.
- Organization name format: lowercase letters, numbers, and underscores only (e.g., `cong_ty_a`, `san_bat_dong_san`).

---

## GET /organizations

Desc: View all organizations.

**Access:** Requires sign-in

**Rules:**
- Returns all organizations (no pagination or filtering).

**Response:** `[Organization]`

---

## GET /organizations/{org_id}

Desc: View organization details.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the organization is not found.

**Response:** `Organization`

---

## POST /organizations

Desc: Create an organization.

**Access:** Admin only

**Rules:**
- Organization name must be unique.
- Organization name must match the format: lowercase letters, numbers, and underscores only.
- Transaction types and property types are stored as linked records.

**Request:** `CreateOrganizationRequest`
**Response:** `Organization` (201)

---

## PUT /organizations/{org_id}

Desc: Update an organization.

**Access:** Admin only

**Rules:**
- Full replace: all organization details must be provided.
- Name uniqueness is checked only if the name has actually changed.

**Request:** `UpdateOrganizationRequest`
**Response:** `Organization`

---

## DELETE /organizations/{org_id}

Desc: Delete an organization.

**Access:** Admin only

**Rules:**
- Cannot delete an organization that has any users assigned to it.
- Permanently deleted (not soft-deleted).

**Response:** 204 No Content

---

## Related

- [Users](./users.md) — organization assignment on user create/update
