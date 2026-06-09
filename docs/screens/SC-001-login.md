# Login

## Purpose

Authenticate users (agents, approvers, admins) to access the platform.

## Route

`/dang-nhap`

## Page Title

Đăng nhập quản lý

## Components

- Logo image (top center)
- Heading: "Đăng nhập"
- Username textbox ("Tên đăng nhập")
- Password textbox ("Mật khẩu")
- "Quên mật khẩu?" link
- "Đăng nhập" submit button

## Validation

- Both fields are required
- Error state: invalid credentials message displayed on submit

## Behaviors

- On success: redirect to homepage (`/`)
- On error: show error message, stay on login page

## Related Stories

- Shared Cart Browsing US-001 (redirect to login when unauthenticated)

## Navigation Links

- None (standalone page, no sidebar)
