# Users

Prefix: `/users`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- All user management requires Admin role.
- Admin accounts are protected: they cannot be created, deleted, deactivated, or have their role changed through the system.
- No one can be promoted to Admin through the system.
- The username cannot be changed after creation.
- Email addresses must be unique.
- New users receive an email with their initial password (sent on create and reset-password).

---

## POST /users

Desc: Create a user account.

**Access:** Admin only

**Rules:**
- Cannot create an Admin account through this action.
- Username must be unique.
- Email must be unique if provided.
- Password must be at least 6 characters.
- If an organization is provided, it must exist.
- New accounts are active by default.
- A welcome email is sent asynchronously if an email is provided.

**Request:** `CreateUserRequest`
**Response:** `UserResponse` (201)

---

## GET /users

Desc: View all user accounts.

**Access:** Admin only

**Rules:**
- Paginated (page default 1, size default 20, max 100).
- Can filter by role, active status, search text, and organization.

**Query Params:** `UserListParams`
**Response:** `UserListResponse`

---

## GET /users/{user_id}

Desc: View user account details.

**Access:** Admin only

**Rules:**
- Returns full user details including avatar, organization name, assigned property types, and assigned transaction types.
- Returns an error if the user is not found.

**Response:** `UserResponse`

---

## PUT /users/{user_id}

Desc: Update a user account.

**Access:** Admin only

**Rules:**
- The username cannot be changed.
- Email uniqueness is enforced if the email is changed.
- An Admin's role cannot be changed.
- No one can be promoted to Admin.
- Property types and transaction types are replaced wholesale when provided.
- Only provided (non-empty) fields are updated.

**Request:** `UpdateUserRequest`
**Response:** `UserResponse`

---

## DELETE /users/{user_id}

Desc: Delete a user account.

**Access:** Admin only

**Rules:**
- Cannot delete an Admin account.
- Permanently deleted (not soft-deleted).

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/deactivate

Desc: Deactivate a user account.

**Access:** Admin only

**Rules:**
- Cannot deactivate an Admin account.
- Sets the account to inactive.

**Response:** `UserResponse`

---

## PATCH /users/{user_id}/reactivate

Desc: Reactivate a user account.

**Access:** Admin only

**Rules:**
- Sets the account back to active.
- No guard against reactivating Admin accounts (unlike deactivate).

**Response:** `UserResponse`

---

## POST /users/{user_id}/reset-password

Desc: Generate a temporary password for a user.

**Access:** Admin only

**Rules:**
- Generates a random 12-character temporary password.
- Stores the hashed password.
- Sends an email with the temporary password if the user has an email on file.

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/change-password

Desc: Set a new password for a user.

**Access:** Admin only

**Rules:**
- New password must be at least 6 characters.
- Sends a password-changed email if the user has an email on file.

**Request:** `ChangeUserPasswordRequest`
**Response:** 204 No Content

---

## POST /users/{user_id}/reset-device

Desc: Clear a user's device binding.

**Access:** Admin only

**Rules:**
- Clears the registered device for the user.
- The user can re-register their device on the next sign-in.

**Response:** `MessageResponse`

---

## Related

- [Auth](./auth.md) — sign-in, device limit, self-service password change
- [Organizations](./organizations.md) — organization assignment
