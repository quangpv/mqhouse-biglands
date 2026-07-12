# Organizations

Prefix: `/organizations`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- List and Get are open to all authenticated users
- Create, Update, Delete require `ADMIN` role
- Update is a full replace (all fields required), not a partial patch
- Name uniqueness enforced on create and on update (only if name actually changed)

---

## GET /organizations

Desc: List all organizations.

**Access:** Authenticated

**Rules:**
- Returns ALL organizations (no pagination, no filtering)

**Response:** `[Organization]`

---

## GET /organizations/{org_id}

Desc: Get organization detail.

**Access:** Authenticated

**Rules:**
- 404 if not found

**Response:** `Organization`

---

## POST /organizations

Desc: Create organization.

**Access:** ADMIN only

**Rules:**
- `name` must be unique (409 if duplicate)
- `transaction_types` and `property_types` stored as junction table records

**Request:** `CreateOrganizationRequest`
**Response:** `Organization` (201)

---

## PUT /organizations/{org_id}

Desc: Update organization.

**Access:** ADMIN only

**Rules:**
- Full replace: all `OrganizationInfo` fields required
- Name uniqueness checked only if name actually changed

**Request:** `UpdateOrganizationRequest`
**Response:** `Organization`

---

## DELETE /organizations/{org_id}

Desc: Delete organization.

**Access:** ADMIN only

**Rules:**
- Cannot delete if ANY users are associated (409 "Cannot delete organization with active users")
- Hard delete

**Response:** 204 No Content

---

## Related

- [Users](./users.md) — organization assignment on user create/update
