# Gap Analysis: SC-010 User Create/Edit

## Against: openapi.yaml

---

## Missing Fields

### 1. `generatedPassword` in create response
- **Screen**: "Create: on success, show user in list with generated password info"
- **API**: `POST /users` returns `User` schema — no password info
- **Impact**: If password is auto-generated, admin cannot communicate it to the new user
- **Fix**: Add optional `generatedPassword: string` to 201 response, present only when password was server-generated and not provided in request

## Missing API

### 1. Password generation strategy
- **Screen**: "Password (create only: auto-generated or manual entry)"
- **API**: `CreateUserRequest` has `password` (required, min 8 chars). No way to signal "auto-generate for me"
- **Impact**: Admin must always enter a password — auto-generation is not supported
- **Fix**: Make `password` optional in `CreateUserRequest`. When omitted, server auto-generates and returns it in the `generatedPassword` response field

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Full name (required) | `CreateUserRequest.fullName` (required, maxLength 255) | ✓ |
| Username (required, unique) | `CreateUserRequest.username` (required, pattern: alphanumeric + underscore) | ✓ |
| Phone (optional) | `UpdateUserRequest.phone` (nullable, maxLength 20) | ✓ |
| Role select (required) | `CreateUserRequest.role` (default AGENT) | ✓ |
| Status toggle (edit only) | `UpdateUserRequest.isActive` | ✓ |
| Edit pre-fill | `GET /users/{id}` → `User` | ✓ |
| Username uniqueness | `POST /users` → 409 Conflict | ✓ |
