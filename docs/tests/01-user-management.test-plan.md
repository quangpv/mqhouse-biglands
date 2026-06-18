# Test Plan: User Management

> **Epic**: User Management  
> **Stories**: US-001-create-user, US-002-edit-user, US-003-deactivate-user, US-004-assign-role  
> **Total BDD Scenarios**: 45  
> **Endpoints**: POST /users, GET /users, GET /users/{id}, PUT /users/{id}, PATCH /users/{id}/deactivate, PATCH /users/{id}/reactivate, PATCH /users/{id}/role

---

## 1. Unit Tests

| ID | Facade | What to Test | Mocked Deps | Assertions |
|----|--------|-------------|-------------|------------|
| UT-UM-01 | `create_user` | Password hash on create | UserRepo, Security | Password is bcrypt-hashed, not plaintext |
| UT-UM-02 | `create_user` | Auto-role default AGENT | UserRepo | role=AGENT when not specified |
| UT-UM-03 | `create_user` | Non-Admin caller raises 403 | UserRepo, current_user(AGENT) | Raises ForbiddenError |
| UT-UM-04 | `create_user` | Duplicate username raises 409 | UserRepo(get_by_username→exists) | Raises ConflictError(USERNAME_TAKEN) |
| UT-UM-05 | `deactivate_user` | Last Admin guard — single admin left | UserRepo(count_active_admins→1) | Raises ConflictError(LAST_ADMIN) |
| UT-UM-06 | `deactivate_user` | Self-deactivation guard | UserRepo, current_user same as target | Raises ForbiddenError |
| UT-UM-07 | `reactivate_user` | Reactivate deactivated user | UserRepo | isActive flips to true |
| UT-UM-08 | `assign_role` | Last Admin guard — changing away from ADMIN | UserRepo(count_active_admins→1) | Raises ConflictError(LAST_ADMIN) |
| UT-UM-09 | `assign_role` | Invalid role enum | Validator | Raises BadRequestError |
| UT-UM-10 | `update_user` | Partial update only changes sent fields | UserRepo | Only provided fields updated |
| UT-UM-11 | `list_users` | Pagination defaults | UserRepo | page=1, size=20 when omitted |
| UT-UM-12 | `list_users` | Role filter passthrough | UserRepo | Correct query param → correct filter |
| UT-UM-13 | `list_users` | Search term passthrough | UserRepo | Search param sent to repo |

**Mapper Tests:**

| ID | Mapper | Input | Assertions |
|----|--------|-------|------------|
| UT-UM-14 | `user_to_response` | UserEntity with all fields | All fields mapped, password_hash excluded |
| UT-UM-15 | `build_user_entity` | CreateUserRequest | Entity has hashed password, created_by_id set |
| UT-UM-16 | `apply_user_update` | UpdateUserRequest + existing entity | Only non-null fields applied |

---

## 2. Integration Tests

| ID | Flow | Setup | Steps | Assertions |
|----|------|-------|-------|------------|
| IT-UM-01 | Create user → DB persists | Admin JWT, clean DB | POST /users → verify in DB | User exists with hashed password |
| IT-UM-02 | Create user → auto-generate password | Admin JWT, password omitted | POST /users | 201, generatedPassword returned |
| IT-UM-03 | Create user → wrong role caller | Agent JWT | POST /users | 403 Forbidden |
| IT-UM-04 | Create user → duplicate username | Admin JWT, existing username | POST /users | 409 USERNAME_TAKEN |
| IT-UM-05 | List users → paginated | Admin JWT, 25 users created | GET /users?page=1&size=10 | 10 items, totalItems=25, totalPages=3 |
| IT-UM-06 | List users → filtered by role | Admin JWT, mix of roles | GET /users?role=APPROVER | Only APPROVER users returned |
| IT-UM-07 | List users → search | Admin JWT, known name | GET /users?search=John | Matching users returned |
| IT-UM-08 | Get user by ID | Admin JWT, existing user | GET /users/{id} | Full user object, password not in response |
| IT-UM-09 | Get user → not found | Admin JWT, random UUID | GET /users/{id} | 404 NOT_FOUND |
| IT-UM-10 | Update user | Admin JWT | PUT /users/{id} with fullName | 200, fullName updated, other fields unchanged |
| IT-UM-11 | Deactivate user | Admin JWT | PATCH /users/{id}/deactivate | 200, isActive=false |
| IT-UM-12 | Deactivate last Admin | Admin JWT (only admin) | PATCH /users/{id}/deactivate | 409 LAST_ADMIN |
| IT-UM-13 | Reactivate user | Admin JWT, deactivated user | PATCH /users/{id}/reactivate | 200, isActive=true |
| IT-UM-14 | Assign role | Admin JWT | PATCH /users/{id}/role | 200, role changed |
| IT-UM-15 | Deactivated user cannot log in | Deactivated user credentials | POST /auth/login | 401 ACCOUNT_DEACTIVATED |

---

## 3. API Tests

| ID | BDD Source | Endpoint | Request | Expected Status | Expected Response |
|----|-----------|----------|---------|-----------------|-------------------|
| AT-UM-01 | US-001 H1 | POST /users | `{fullName, username, password}` | 201 | User with role=AGENT |
| AT-UM-02 | US-001 H2 | POST /users | `{..., role:APPROVER}` | 201 | User with role=APPROVER |
| AT-UM-03 | US-001 H3 | POST /users | Auto-generated password | 201 | generatedPassword in response |
| AT-UM-04 | US-001 E1 | POST /users | `{fullName, password}` (no username) | 400 | VALIDATION_ERROR, field=username |
| AT-UM-05 | US-001 E2 | POST /users | `{username, password}` (no fullName) | 400 | VALIDATION_ERROR, field=fullName |
| AT-UM-06 | US-001 E3 | POST /users | `{username: "exists", fullName, password}` | 409 | USERNAME_TAKEN |
| AT-UM-07 | US-001 E4 | POST /users | `{fullName, username, password: "short"}` | 400 | VALIDATION_ERROR, field=password |
| AT-UM-08 | US-001 S1 | POST /users | No auth header | 401 | UNAUTHORIZED |
| AT-UM-09 | US-001 S2 | POST /users | Agent token | 403 | FORBIDDEN |
| AT-UM-10 | US-001 S3 | POST /users | Expired token | 401 | UNAUTHORIZED |
| AT-UM-11 | US-001 S4 | POST /users | Agent tries create APPROVER | 403 | FORBIDDEN |
| AT-UM-12 | US-002 H1 | PUT /users/{id} | `{fullName: "New Name"}` | 200 | fullName updated |
| AT-UM-13 | US-002 H2 | PUT /users/{id} | `{phone: "0912345678"}` | 200 | phone updated |
| AT-UM-14 | US-002 H3 | PUT /users/{id} | `{email: "a@b.com"}` | 200 | email updated |
| AT-UM-15 | US-002 H4 | PUT /users/{id} | `{phone: "", email: ""}` | 200 | phone=null, email=null |
| AT-UM-16 | US-002 E1 | PUT /users/{id} | `{username: "taken"}` | 409 | USERNAME_TAKEN |
| AT-UM-17 | US-002 S1 | PUT /users/{id} | Agent token on other user | 403 | FORBIDDEN |
| AT-UM-18 | US-002 S2 | PUT /users/{id} | Non-Admin token | 403 | FORBIDDEN |
| AT-UM-19 | US-002 S3 | PUT /users/{id} | No auth | 401 | UNAUTHORIZED |
| AT-UM-20 | US-003 H1 | PATCH /users/{id}/deactivate | Admin token, agent target | 200 | isActive=false |
| AT-UM-21 | US-003 H2 | PATCH /users/{id}/deactivate | Admin deactivates another Admin | 200 | isActive=false |
| AT-UM-22 | US-003 H3 | PATCH /users/{id}/reactivate | Admin token, deactivated target | 200 | isActive=true |
| AT-UM-23 | US-003 H4 | PATCH /users/{id}/deactivate | Target already inactive | 200 | isActive=false (idempotent) |
| AT-UM-24 | US-003 E1 | PATCH /users/{id}/deactivate | Target is last Admin | 409 | LAST_ADMIN |
| AT-UM-25 | US-003 E2 | PATCH /users/{id}/reactivate | Target already active | 200 | isActive=true (idempotent) |
| AT-UM-26 | US-003 S1 | PATCH /users/{id}/deactivate | Non-Admin | 403 | FORBIDDEN |
| AT-UM-27 | US-003 S2 | PATCH /users/{id}/deactivate | No auth | 401 | UNAUTHORIZED |
| AT-UM-28 | US-004 H1 | PATCH /users/{id}/role | `{role: APPROVER}` | 200 | role changed |
| AT-UM-29 | US-004 H2 | PATCH /users/{id}/role | `{role: ADMIN}` | 200 | role changed |
| AT-UM-30 | US-004 H3 | PATCH /users/{id}/role | `{role: AGENT}` | 200 | role changed |
| AT-UM-31 | US-004 E1 | PATCH /users/{id}/role | `{role: INVALID}` | 400 | VALIDATION_ERROR |
| AT-UM-32 | US-004 S1 | PATCH /users/{id}/role | Non-Admin | 403 | FORBIDDEN |
| AT-UM-33 | US-004 S2 | PATCH /users/{id}/role | Last Admin → AGENT | 409 | LAST_ADMIN |

---

## 4. Security Tests

| ID | BDD Source | Scenario | Endpoint | Expected Status |
|----|-----------|----------|----------|-----------------|
| SC-UM-01 | US-001 S1 | No token | POST /users | 401 |
| SC-UM-02 | US-001 S2 | Agent token | POST /users | 403 |
| SC-UM-03 | US-001 S3 | Expired/malformed token | POST /users | 401 |
| SC-UM-04 | US-001 S4 | Agent tries create APPROVER | POST /users | 403 |
| SC-UM-05 | US-002 S1 | Agent edits other user | PUT /users/{id} | 403 |
| SC-UM-06 | US-003 S1 | Agent deactivates user | PATCH /users/{id}/deactivate | 403 |
| SC-UM-07 | US-003 S2 | No token deactivates | PATCH /users/{id}/deactivate | 401 |
| SC-UM-08 | US-004 S1 | Agent assigns role | PATCH /users/{id}/role | 403 |
| SC-UM-09 | US-004 S3 | Approver assigns ADMIN | PATCH /users/{id}/role | 403 |
| SC-UM-10 | — | SQL injection in search | GET /users?search=`' OR 1=1 --` | 200 (sanitized, no extra data) |
| SC-UM-11 | — | XSS in fullName | POST /users `fullName: "<script>..."` | 201 (stored escaped or rejected) |

---

## 5. Load Tests

| ID | Scenario | Concurrent Users | Target | Duration |
|----|----------|-----------------|--------|----------|
| LD-UM-01 | Bulk user creation (Admin) | 10 | 50 req/s, p95 < 500ms | 2 min |
| LD-UM-02 | List users with search | 20 | 100 req/s, p95 < 300ms | 2 min |
| LD-UM-03 | Concurrent role assignments on same user | 5 | No corrupt state (last-Admin guard holds) | 30s |
