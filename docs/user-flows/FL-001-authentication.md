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

- **Forgot password**: User clicks "Quên mật khẩu?" (not implemented in current scope — rely on admin reset)
- **Already authenticated**: Redirect directly to `/` from login page

## Notes

- Page title shows "Đăng nhập quản lý" on the login page, but "Biglands" on all other pages after authentication
- After successful login, user name appears in the top banner with avatar

## Screen References

- SC-001 Login

## Story References

- Shared Cart Browsing US-001 (redirect to login when unauthenticated)
