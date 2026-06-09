# User Create / Edit

## Purpose

Create a new user or edit an existing user's profile.

## Route

Create: `/admin/quan-ly-nguoi-dung/tao`
Edit: `/admin/quan-ly-nguoi-dung/:id/sua`

## Form Fields

- Full name (required)
- Username (required, unique)
- Phone (optional)
- Role (select: AGENT / APPROVER / ADMIN — required)
- Password (create only: auto-generated or manual entry)
- Status toggle: Active / Inactive (edit only)

## Validation

- Username must be unique
- All required fields validated before submit
- Password minimum length (if manual)

## Behaviors

- Create: on success, show user in list with generated password info
- Edit: on success, return to user list
- Deactivate: confirmation dialog before changing status

## Entities

- User

## Related Stories

- User Management US-001 (create), US-002 (edit)

## Navigation Links

- User Management List `/admin/quan-ly-nguoi-dung`
