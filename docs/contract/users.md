# Users

Prefix: `/users`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- All user management requires Admin role.
- Admin accounts are protected: they cannot be created, deleted, deactivated, or have their role changed through the system.
- No one can be promoted to Admin through the system.
- The username cannot be changed after creation.
- Email addresses must be unique across active users. Usernames and emails of deleted users become available for reuse.
- New users receive an email with their initial password (sent on create and reset-password).
- Soft-deleted users are hidden from all user lists and queries. Administrators cannot view, edit, or manage soft-deleted users (except to restore them).
- A user's properties, reviews, and files remain available to other users after deletion.
- A user may hold optional **permissions** that control whether they (as a Sales user) can view restricted fields on properties they did not create. See the catalog endpoint `GET /permissions` and [Properties](./properties.md) for how permissions affect visibility.

---

## POST /users

Desc: Create a user account.

**Access:** Admin only

**Rules:**
- Cannot create an Admin account through this action.
- Username must be unique among active users. A username previously used by a deleted user can be reused.
- Email must be unique among active users if provided. An email previously used by a deleted user can be reused.
- Password must be at least 6 characters.
- If an organization is provided, it must exist.
- New accounts are active by default.
- A welcome email is sent asynchronously if an email is provided.
- Permissions may be assigned on creation; unknown permission codes are rejected.

**Request:** `CreateUserRequest`
**Response:** `UserResponse` (201)

---

## GET /users

Desc: View all user accounts.

**Access:** Admin only

**Rules:**
- Paginated (page default 1, size default 20, max 100).
- Can filter by role, active status, search text, and organization.
- Soft-deleted users are excluded from results.

**Query Params:** `UserListParams`
**Response:** `UserListResponse`

---

## GET /users/{user_id}

Desc: View user account details.

**Access:** Admin only

**Rules:**
- Returns full user details including avatar, organization name, assigned property types, assigned transaction types, and assigned permissions.
- Returns "User not found" if the user is not found or has been soft-deleted.

**Response:** `UserResponse`

---

## PUT /users/{user_id}

Desc: Update a user account.

**Access:** Admin only

**Rules:**
- The username cannot be changed.
- Email uniqueness is enforced among active users if the email is changed.
- An Admin's role cannot be changed.
- No one can be promoted to Admin.
- Property types and transaction types are replaced wholesale when provided.
- Permissions are replaced wholesale when provided; unknown permission codes are rejected.
- Only provided (non-empty) fields are updated.
- Cannot update a soft-deleted user.

**Request:** `UpdateUserRequest`
**Response:** `UserResponse`

---

## DELETE /users/{user_id}

Desc: Delete a user account.

**Access:** Admin only

**Rules:**
- Cannot delete an Admin account.
- Before deletion, the system checks if the user has created any data in these tables: properties, approvals, hot listings, notifications, or reviews.
- If the user **has** references in any of these tables, the account is **soft deleted** — a `deleted_at` timestamp is set and the user is hidden from normal queries, but the record and its data are preserved.
- If the user **has no** references in any of these tables, the account is **permanently removed** from the database.

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/deactivate

Desc: Deactivate a user account.

**Access:** Admin only

**Rules:**
- Cannot deactivate an Admin account.
- Cannot deactivate a soft-deleted user.
- Sets the account to inactive.

**Response:** `UserResponse`

---

## PATCH /users/{user_id}/reactivate

Desc: Reactivate a user account.

**Access:** Admin only

**Rules:**
- Sets the account back to active.
- Can restore a soft-deleted user — clears the deleted status and makes the user visible again.
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
- Cannot reset password for a soft-deleted user.

**Response:** `MessageResponse`

---

## PATCH /users/{user_id}/change-password

Desc: Set a new password for a user.

**Access:** Admin only

**Rules:**
- New password must be at least 6 characters.
- Sends a password-changed email if the user has an email on file.
- Cannot change password for a soft-deleted user.

**Request:** `ChangeUserPasswordRequest`
**Response:** 204 No Content

---

## POST /users/{user_id}/reset-device

Desc: Clear a user's device binding.

**Access:** Admin only

**Rules:**
- Clears the registered device for the user.
- The user can re-register their device on the next sign-in.
- Cannot reset device for a soft-deleted user.

**Response:** `MessageResponse`

---

## Related

- [Auth](./auth.md) — sign-in, device limit, self-service password change
- [Organizations](./organizations.md) — organization assignment
