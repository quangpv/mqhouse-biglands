# Gap Analysis: SC-001 Login

## Against: openapi.yaml

---

## Missing APIs

### 1. Forgot Password
- **Screen**: "Quên mật khẩu?" link is displayed below the password field
- **API**: No `POST /auth/forgot-password` or `POST /auth/reset-password` endpoint exists in openapi.yaml
- **Impact**: Link has no backend action — must either implement the endpoint or remove the link from the screen
- **Priority**: Should Have (blocked UX path)

## Missing States

### 1. Deactivated Account Error Code
- **Screen**: Shows generic error message on invalid credentials
- **API**: `LoginResponse` 401 returns `UNAUTHORIZED` with no distinction between "wrong password" and "account deactivated"
- **Domain Model**: USR-I02 states "A user with isActive = false must be rejected at login with 'account deactivated' error"
- **Impact**: User cannot distinguish between credential error and deactivation; support tickets may increase
- **Fix**: Add `ACCOUNT_DEACTIVATED` error code (403 or a 401 variant with specific `code` field)

## Inconsistent Naming

None — screen route `/dang-nhap` is a frontend path, backed by `POST /auth/login`. The separation between FE routes (Vietnamese) and API paths (English) is acceptable.

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Username field | `LoginRequest.username` | ✓ |
| Password field | `LoginRequest.password` | ✓ |
| Submit → login | `POST /auth/login` → 200 `LoginResponse.token` | ✓ |
| Redirect to `/` | LoginResponse returns user data | ✓ |
