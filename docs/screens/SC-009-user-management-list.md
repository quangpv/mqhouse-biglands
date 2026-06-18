# User Management List

## Purpose

View all platform users, search, and manage their accounts.

## Route

`/admin/quan-ly-nguoi-dung`

## Components

### Header
- Title: "Quản lý người dùng"
- "Create User" button

### Table
Columns:
- Full name
- Username
- Phone
- Role (displays organization/team names like "MQ Land", "ID Land" — not AGENT/APPROVER/ADMIN enum values as documented in entity definitions)
- Status (Active / Inactive badge)
- Created date
- Actions (Edit, Deactivate/Activate)

### Search
- Search by name, username, or phone

### Pagination
- Page navigation for large user lists

## Entities

- User

## Related Stories

- User Management US-001 (create), US-002 (edit), US-003 (deactivate), US-004 (assign role)

## Navigation Links

- User Create/Edit `/admin/quan-ly-nguoi-dung/tao` or `/admin/quan-ly-nguoi-dung/:id/sua`
- Shared Cart Home `/`
