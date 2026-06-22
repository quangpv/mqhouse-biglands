# Authentication

## Goal

Authenticate user to access the platform.

## Trigger

User navigates to any protected route while unauthenticated.

## Preconditions

- User has an active account (created by admin)
- User knows their username and password

## Main Flow

```mermaid
flowchart TD
    A[User navigates to /dang-nhap] --> B[Enter username]
    B --> C[Enter password]
    C --> D[Click "Đăng nhập"]
    D --> E{Validate credentials}
    E -->|Valid| F[Redirect to /]
    E -->|Invalid| G[Show error message]
    G --> B
```

## Alternative Flows

- **Forgot password**: User clicks "Quên mật khẩu?" → enters registered email → receives JWT reset link → clicks link → enters new password + confirmation → password updated, redirect to login
- **Already authenticated**: Redirect directly to `/` from login page

## Notes

- Page title shows "Đăng nhập quản lý" on the login page, but "Biglands" on all other pages after authentication
- After successful login, user name appears in the top banner with avatar
- Forgot/reset password implemented via JWT tokens (no DB schema change needed):
  - `POST /api/v1/auth/forgot-password` — accepts email, sends reset link
  - `POST /api/v1/auth/reset-password` — accepts token + new password, updates password hash

## Screen References

- SC-001 Login

## Story References

- Shared Cart Browsing US-001 (redirect to login when unauthenticated)
