# Auth + Profile

Prefix: `/auth`, `/me`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

### Token Lifecycle
- Users stay signed in for 24 hours.
- Refresh sessions last 7 days and allow automatic re-authentication.
- Password reset links expire after 15 minutes.
- Each refresh session can only be used once. A new one is issued automatically after each refresh.
- Signing out cancels the current session and all other active sessions for that user.
- Changing your password does not invalidate existing sessions.

### Device Limit
- Only enforced for Sales staff and Approvers.
- Admins are always exempt, even when device limiting is enabled.
- First sign-in with device limiting registers the device.
- Subsequent sign-ins must match the registered device, otherwise access is denied.
- When device limiting is disabled, the device check is completely ignored.
- The device token is provided via the `X-Device-Token` header during sign-in.
- If the device token does not match the registered device, sign-in is denied with a "Device mismatch" error.

### Password Constraints
- Sign-in password: minimum 1 character.
- Change, reset, or create password: minimum 6 characters.
- A password reset link can be reused multiple times within the 15-minute window.

### User Enumeration Protection
- Sign-in returns the same "Invalid credentials" message for both wrong username and wrong password.
- Forgot-password returns "User not found" for emails that do not exist in the system (this reveals whether an email is registered).

---

## POST /auth/login

Desc: Sign in with username or email.

**Access:** Public

**Rules:**
- If the input contains `@`, it is treated as an email; otherwise as a username.
- Returns "Invalid credentials" for both wrong username/email and wrong password.
- Returns "Account is deactivated" if the account has been deactivated.
- Device limit enforcement applies for Sales staff and Approvers (see Global Rules).
- On success: issues a signed-in session and a refresh session.

**Request:** `LoginRequest`
**Response:** `LoginResponse`

---

## POST /auth/refresh

Desc: Refresh your session and get a new signed-in session.

**Access:** Public (request body contains the refresh session token)

**Rules:**
- Verifies the token is a valid refresh session.
- Checks the refresh session has not been revoked.
- Checks the user exists and is active.
- On success: revokes the old refresh session, issues a new signed-in session and refresh session.

**Request:** `RefreshTokenRequest`
**Response:** `RefreshTokenResponse`

---

## POST /auth/logout

Desc: Sign out — cancel current session and all other active sessions.

**Access:** Requires sign-in

**Rules:**
- Cancels the current signed-in session.
- Revokes all refresh sessions for the user.

**Response:** `MessageResponse`

---

## POST /auth/change-password

Desc: Change your own password.

**Access:** Requires sign-in

**Rules:**
- Current password must match the one on file, otherwise the request is rejected.
- New password must be at least 6 characters.
- Does not invalidate existing sessions.

**Request:** `ChangePasswordRequest`
**Response:** `MessageResponse`

---

## POST /auth/forgot-password

Desc: Request a password reset email.

**Access:** Public

**Rules:**
- Looks up the user by email; returns "User not found" if the email is not registered.
- Generates a password reset link (valid for 15 minutes).
- Sends the email asynchronously if the user has an email on file; silently skips if no email is set.
- No rate limiting is applied.

**Request:** `ForgotPasswordRequest`
**Response:** `MessageResponse`

---

## POST /auth/reset-password

Desc: Reset your password using a link from your email.

**Access:** Public

**Rules:**
- The reset link must be valid and not expired (within 15-minute window).
- Returns an error for invalid or expired links.
- Updates the password on file.
- Does not invalidate existing sessions.
- The same reset link can be reused multiple times within the 15-minute window.

**Request:** `ResetPasswordRequest`
**Response:** `MessageResponse`

---

## GET /me

Desc: View your own profile.

**Access:** Requires sign-in

**Rules:**
- Always returns the current user's own data.
- Includes: avatar, organization name, assigned property types, assigned transaction types, and device limit setting.

**Response:** `ProfileResponse`

---

## GET /me/properties

Desc: View your own properties.

**Access:** Requires sign-in

**Rules:**
- Only returns properties you created.
- Supports filtering by status, district, price range, text search.
- Each property indicates whether you have pinned it.

**Query Params:** `PropertyListParams` (without `created_by_id`)
**Response:** `PropertyListResponse`

---

## GET /me/hots

Desc: View your own hot (featured) properties.

**Access:** Requires sign-in

**Rules:**
- Same as your properties, but only shows your hot (featured) properties.
- Each property indicates whether you have pinned it.

**Response:** `PropertyListResponse`

---

## GET /me/properties/rejected

Desc: View your rejected properties.

**Access:** Requires sign-in

**Rules:**
- Same as your properties, but only shows properties that were rejected by an approver.

**Response:** `PropertyListResponse`

---

## GET /me/pins

Desc: View your pinned properties.

**Access:** Requires sign-in

**Rules:**
- Returns only properties you have pinned.
- All returned properties indicate they are pinned.
- Supports the same filters as property listing.

**Response:** `PropertyListResponse`

---

## Related

- [Properties](./properties.md) — property listings, status changes, history
- [Users](./users.md) — admin user management
- [Notifications](./notifications.md) — notification preferences
