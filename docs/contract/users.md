# Users

Prefix: `/users`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- All user management endpoints require `ADMIN` role
- `ADMIN` role is protected: cannot create ADMIN, cannot delete ADMIN, cannot deactivate ADMIN, cannot change role of ADMIN, cannot upgrade anyone to ADMIN
- Username is immutable after creation
- Email uniqueness enforced on both create and update
- Welcome email contains plaintext password (sent on create and reset-password)

---

## POST /users

Desc: Create user.

**Access:** ADMIN only

**Rules:**
- Cannot create ADMIN role (403)
- Username must be unique (409)
- Email must be unique if provided (409)
- Password min 6 characters
- If `organization_id` provided, org must exist (404)
- Default `is_active=true`
- Welcome email sent asynchronously if email provided

**Request:** `CreateUserRequest`
**Response:** `UserResponse` (201)

---

## GET /users

Desc: List users.

**Access:** ADMIN only

**Rules:**
- Paginated (page default 1, size default 20, max 100)
- Filterable by role, is_active, search, organization_id

**Query Params:** `UserListParams`
**Response:** `UserListResponse`

---

## GET /users/{user_id}

Desc: Get user detail.

**Access:** ADMIN only

**Rules:**
- Returns full user with avatar_url, organization_name, property_type_ids, transaction_type_ids
- 404 if not found

**Response:** `UserResponse`

---

## PUT /users/{user_id}

Desc: Update user.

**Access:** ADMIN only

**Rules:**
- Username is NOT updatable
- Email uniqueness enforced if changed
- Cannot change role of an ADMIN (403)
- Cannot upgrade anyone to ADMIN (403)
- `property_type_ids` and `transaction_type_ids` replaced wholesale when provided
- Only provided (non-None) fields are updated

**Request:** `UpdateUserRequest`
**Response:** `UserResponse`

---

## DELETE /users/{user_id}

Desc: Delete user.

**Access:** ADMIN only

**Rules:**
- Cannot delete ADMIN (403)
- Hard delete (not soft delete)

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/deactivate

Desc: Deactivate user.

**Access:** ADMIN only

**Rules:**
- Cannot deactivate ADMIN (403)
- Sets `is_active=false`

**Response:** `UserResponse`

---

## PATCH /users/{user_id}/reactivate

Desc: Reactivate user.

**Access:** ADMIN only

**Rules:**
- Sets `is_active=true`
- No guard against reactivating ADMIN (unlike deactivate)

**Response:** `UserResponse`

---

## POST /users/{user_id}/reset-password

Desc: Generate temporary password.

**Access:** ADMIN only

**Rules:**
- Generates random 12-character temp password
- Hashes and stores it
- Sends email with plaintext temp password if user has email

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/change-password

Desc: Admin set new password for user.

**Access:** ADMIN only

**Rules:**
- `new_password` min 6 characters
- Sends password-changed email if user has email

**Request:** `ChangeUserPasswordRequest`
**Response:** 204 No Content

---

## POST /users/{user_id}/reset-device

Desc: Clear device binding.

**Access:** ADMIN only

**Rules:**
- Sets `device_id=null`
- User can re-register device on next login

**Response:** `MessageResponse`

---

## Related

- [Auth](./auth.md) — login, device limit, self-service password change
- [Organizations](./organizations.md) — organization assignment
