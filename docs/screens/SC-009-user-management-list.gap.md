# Gap Analysis: SC-009 User Management List

## Against: openapi.yaml

---

## Missing Fields

### 1. `organizationName` / team
- **Screen**: Role column displays organization/team names ("MQ Land", "ID Land") — not the enum values AGENT/APPROVER/ADMIN
- **Schema**: `User` has `role` (enum: AGENT/APPROVER/ADMIN) only — no organization association
- **Domain Model**: G-03 identifies this as a gap: "Organization/Team concept absent. Role column in user list (SC-009) shows org names not enum values."
- **Impact**: The screen literally cannot render the data it shows. The column displays data that has no backend representation
- **Priority**: Must Have (screen displays data that doesn't exist in the model)
- **Fix**: Define an `Organization` entity with `name` and `displayName`, or add `displayRole: string` to `User` that allows custom display names per-instance

### 2. `generatedPassword` in create response
- **Screen**: The page implies admin sees generated password info after creating a user (redirect to user list with password info)
- **Schema**: `POST /users` returns `User` — no `generatedPassword` field
- **Fix**: Add optional `generatedPassword: string` to the 201 response, present only when password was auto-generated

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Table: full name | `User.fullName` (maxLength: 255) | ✓ |
| Table: username | `User.username` (maxLength: 100) | ✓ |
| Table: phone | `User.phone` (maxLength: 20, nullable) | ✓ |
| Table: role | `User.role` (AGENT/APPROVER/ADMIN) | ✓ (gap above for display) |
| Table: status (Active/Inactive) | `User.isActive` | ✓ |
| Table: created date | `User.createdAt` (date-time) | ✓ |
| Table: Edit action | `PUT /users/{id}` | ✓ |
| Table: Deactivate/Activate | `PATCH /users/{id}/deactivate` / `PATCH /users/{id}/reactivate` | ✓ |
| Search | `GET /users?search=` | ✓ |
| Pagination | `page` + `size` params | ✓ |
| Create button | FE route `/admin/quan-ly-nguoi-dung/tao` | ✓ |
| Last-Admin protection | `409` error on deactivate/role-change of last Admin | ✓ |
