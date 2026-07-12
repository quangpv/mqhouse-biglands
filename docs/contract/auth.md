# Auth + Profile

Prefix: `/auth`, `/me`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

### Token Lifecycle
- Access token TTL: 24 hours (`jwt_expire_minutes=1440`)
- Refresh token TTL: 7 days (`jwt_refresh_expire_minutes=10080`)
- Reset token TTL: 15 minutes (hardcoded)
- Refresh tokens are single-use (rotation on each refresh)
- Logout = blacklisted access token JTI + all refresh tokens revoked
- Change password does NOT invalidate existing tokens

### Device Limit
- Only enforced for `SALE` and `APPROVER` roles
- `ADMIN` is always exempt (even when `device_limit_enabled=true`)
- First login with device_limit registers `X-Device-Token` header value
- Subsequent logins must match registered device (403 on mismatch)
- When `device_limit_enabled=false`, header is completely ignored

### Password Constraints
- Login password: min 1 character
- Change/reset/create password: min 6 characters
- Reset token not invalidated after use (reusable within 15-min window)

### User Enumeration Protection
- Login returns identical "Invalid credentials" for both wrong user and wrong password
- Forgot-password returns 404 "User not found" for nonexistent emails (leaks existence)

---

## POST /auth/login

Desc: Login with username or email.

**Access:** Public

**Rules:**
- If `username` contains `@`, looks up by email; otherwise by username
- Returns 401 "Invalid credentials" for both wrong user and wrong password
- Returns 401 "Account is deactivated" if `is_active=false`
- Device limit enforcement (see Global Rules above)
- On success: generates access + refresh tokens, stores refresh token hash in DB

**Request:** `LoginRequest`
**Response:** `LoginResponse`

---

## POST /auth/refresh

Desc: Rotate refresh token and get new access token.

**Access:** Public (body contains refresh token)

**Rules:**
- Decodes token, checks `purpose == "refresh"`
- Checks token is not revoked in `refresh_tokens` table
- Checks user exists and is active
- On success: revokes old refresh token, issues new access + refresh pair

**Request:** `RefreshTokenRequest`
**Response:** `RefreshTokenResponse`

---

## POST /auth/logout

Desc: Full logout — blacklist current access token + revoke all refresh tokens.

**Access:** Authenticated

**Rules:**
- Adds current token's JTI to `token_blacklist`
- Revokes ALL refresh tokens for the user

**Response:** `MessageResponse`

---

## POST /auth/change-password

Desc: Change current user's password.

**Access:** Authenticated

**Rules:**
- `current_password` must match stored hash (400 "Current password is incorrect")
- `new_password` min 6 characters
- Does NOT invalidate existing tokens

**Request:** `ChangePasswordRequest`
**Response:** `MessageResponse`

---

## POST /auth/forgot-password

Desc: Request password reset email.

**Access:** Public

**Rules:**
- Looks up user by email; returns 404 if not found
- Generates reset JWT (purpose=`password_reset`, 15-min TTL)
- Sends email asynchronously if user has email; silently skips if no email
- No rate limiting

**Request:** `ForgotPasswordRequest`
**Response:** `MessageResponse`

---

## POST /auth/reset-password

Desc: Reset password with token from email.

**Access:** Public

**Rules:**
- Validates token: must decode, must have `purpose=password_reset`
- Returns 400 for invalid/expired tokens
- Updates `password_hash`
- Does NOT revoke existing tokens
- Token reusable within 15-min window

**Request:** `ResetPasswordRequest`
**Response:** `MessageResponse`

---

## GET /me

Desc: Get current user's profile.

**Access:** Authenticated

**Rules:**
- Always returns the caller's own data
- Response includes: avatar_url, organization_name, property_type_ids, transaction_type_ids, device_limit_enabled

**Response:** `ProfileResponse`

---

## GET /me/properties

Desc: List current user's properties.

**Access:** Authenticated

**Rules:**
- Only returns properties owned by the current user
- Supports filtering by status, district, price range, text search
- Each property includes `is_pinned` flag

**Query Params:** `PropertyListParams` (without `created_by_id`)
**Response:** `PropertyListResponse`

---

## GET /me/hots

Desc: List current user's hot properties.

**Access:** Authenticated

**Rules:**
- Same as `/me/properties` but filtered to hot properties only
- Each property includes `is_pinned` flag

**Response:** `PropertyListResponse`

---

## GET /me/properties/rejected

Desc: List current user's rejected properties.

**Access:** Authenticated

**Rules:**
- Same scoping as `/me/properties` but filtered to rejected properties

**Response:** `PropertyListResponse`

---

## GET /me/pins

Desc: List current user's pinned properties.

**Access:** Authenticated

**Rules:**
- Returns properties pinned by the current user only
- All returned properties have `is_pinned=true`
- Supports same filters as property list

**Response:** `PropertyListResponse`

---

## Related

- [Properties](./properties.md) — property CRUD, transitions, status logs
- [Users](./users.md) — admin user management
- [Notifications](./notifications.md) — notification preferences
