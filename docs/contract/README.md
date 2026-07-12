# API Contract

Business rules for all Biglands APIs, organized by domain.

## Global Rules

### Authentication
- All endpoints require JWT Bearer token unless marked **Public**.
- Token passed via `Authorization: Bearer <token>` header.
- Access token TTL: 24 hours. Refresh token TTL: 7 days.
- Refresh tokens are single-use (rotation on each refresh).
- Logout invalidates current access token (JTI blacklisted) AND all refresh tokens for the user.

### Authorization
- Three roles: `SALE`, `APPROVER`, `ADMIN`.
- `require_role(*roles)` returns 403 if user role not in allowed list.
- Deactivated users (`is_active=false`) get 401 on any authenticated endpoint.

### Error Responses
| Exception | HTTP Status |
|---|---|
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `BadRequestError` | 400 |
| `UnauthorizedError` | 401 |
| `ForbiddenError` | 403 |

### Pagination
- `page` (default 1, min 1), `size` (default 20, min 1, max 100).
- Response includes `metadata: { page, size, total_pages, total_items }`.

### Phone Masking
- For `SALE` users viewing properties they did NOT create: `creator.phone` and `owner_phone` are masked (first 4 digits + `****`).
- `ADMIN`/`APPROVER` and property owners always see full phone numbers.

---

## RBAC Matrix

| Endpoint | ADMIN | APPROVER | SALE | Public |
|---|---|---|---|---|
| **Auth** | | | | |
| `POST /auth/login` | - | - | - | Y |
| `POST /auth/refresh` | - | - | - | Y |
| `POST /auth/forgot-password` | - | - | - | Y |
| `POST /auth/reset-password` | - | - | - | Y |
| `POST /auth/logout` | Y | Y | Y | - |
| `POST /auth/change-password` | Y | Y | Y | - |
| `GET /me` | Y | Y | Y | - |
| **Properties** | | | | |
| `POST /properties` | Y | Y | Y | - |
| `GET /properties` | Y | Y | Y | - |
| `GET /properties/counts` | Y | Y | Y | - |
| `GET /properties/{id}` | Y | Y | Y | - |
| `PUT /properties/{id}` | Y* | Y* | Owner only | - |
| `DELETE /properties/{id}` | Y (any) | Owner only | Owner only | - |
| `POST /properties/{id}/transitions/*` | Y** | Y** | Owner only*** | - |
| `GET /properties/{id}/status-logs` | Y | Y | Y | - |
| **Approvals** | | | | |
| `GET /approvals` | Y | Y | 403 | - |
| `GET /approvals/counts` | Y | Y | 403 | - |
| `GET /properties/{id}/pending-approval` | Y | Y | Y | - |
| `POST /approvals/{id}/approve` | Y | Y | 403 | - |
| `POST /approvals/{id}/reject` | Y | Y | 403 | - |
| **Users** | | | | |
| `POST /users` | Y | 403 | 403 | - |
| `GET /users` | Y | 403 | 403 | - |
| `GET /users/{id}` | Y | 403 | 403 | - |
| `PUT /users/{id}` | Y | 403 | 403 | - |
| `DELETE /users/{id}` | Y | 403 | 403 | - |
| `PATCH /users/{id}/deactivate` | Y | 403 | 403 | - |
| `PATCH /users/{id}/reactivate` | Y | 403 | 403 | - |
| `POST /users/{id}/reset-password` | Y | 403 | 403 | - |
| `PATCH /users/{id}/change-password` | Y | 403 | 403 | - |
| `POST /users/{id}/reset-device` | Y | 403 | 403 | - |
| **Organizations** | | | | |
| `GET /organizations` | Y | Y | Y | - |
| `GET /organizations/{id}` | Y | Y | Y | - |
| `POST /organizations` | Y | 403 | 403 | - |
| `PUT /organizations/{id}` | Y | 403 | 403 | - |
| `DELETE /organizations/{id}` | Y | 403 | 403 | - |
| **Files** | | | | |
| `POST /files` | Y | Y | Y | - |
| `GET /files/{id}` | Y | Y | Y | - |
| `DELETE /files/{id}` | Y (any) | Owner only | Owner only | - |
| **Reviews** | | | | |
| `GET /properties/{id}/reviews` | Y | Y | Y | - |
| `POST /properties/{id}/reviews` | Y | Y | Y | - |
| `DELETE /properties/{id}/reviews/{rid}` | Y (any) | Owner only | Owner only | - |
| **Hot Properties** | | | | |
| `GET /properties/hots` | Y | Y | Y | - |
| `POST /properties/{id}/hots` | Y | 403 | 403 | - |
| `DELETE /properties/{id}/hots` | Y | 403 | 403 | - |
| **Pins** | | | | |
| `POST /properties/{id}/pins` | Y | Y | Y | - |
| `DELETE /properties/{id}/pins` | Y | Y | Y | - |
| `GET /me/pins` | Y | Y | Y | - |
| **Notifications** | | | | |
| `GET /notifications` | Y | Y | Y | - |
| `GET /notifications/counts` | Y | Y | Y | - |
| `PATCH /notifications/{id}/read` | Y | Y | Y | - |
| `PATCH /notifications/read-all` | Y | Y | Y | - |
| `GET /me/notification-preferences` | Y | Y | Y | - |
| `PUT /me/notification-preferences` | Y | Y | Y | - |
| **Meta Data** | | | | |
| `GET /transaction-types` | Y | Y | Y | - |
| `POST /transaction-types` | Y | 403 | 403 | - |
| `PUT /transaction-types/{id}` | Y | 403 | 403 | - |
| `DELETE /transaction-types/{id}` | Y | 403 | 403 | - |
| `GET /property-types` | Y | Y | Y | - |
| `POST /property-types` | Y | 403 | 403 | - |
| `PUT /property-types/{id}` | Y | 403 | 403 | - |
| `DELETE /property-types/{id}` | Y | 403 | 403 | - |
| `GET /tags` | Y | Y | Y | - |
| `POST /tags` | Y | 403 | 403 | - |
| `PUT /tags/{id}` | Y | 403 | 403 | - |
| `DELETE /tags/{id}` | Y | 403 | 403 | - |
| **System** | | | | |
| `GET /geography/*` | - | - | - | Y |
| `GET /master-data` | Y | Y | Y | - |
| `GET /supports` | Y | Y | Y | - |
| `POST /backfills` | Y | 403 | 403 | - |
| `GET /backfills` | Y | 403 | 403 | - |
| `GET /ws?token=...` | Y | Y | Y | - |
| **Carts** | | | | |
| `GET /carts/counts` | Y | Y | Y | - |

\* SALE: owner only, ADMIN/APPROVER: any
\** SALE: owner only, ADMIN/APPROVER: any
\*** Submit/withdraw/deposit/soldout/cancel/complete/reopen: SALE must be owner

---

## Property State Machine

```
                          (ADMIN/APPROVER submit)
DRAFT ──────────────────────────────────────────────> AVAILABLE
  │                                                       │
  │ (SALE submit)                                         │
  └──────────────> POST_PENDING ──(approve)───────────────┘
                         │         (reject)
                         │            │
                         │            └──> DRAFT
                         │ (SALE withdraw)
                         └──> DRAFT

                         AVAILABLE ──(admin soldout)──> SOLDOUT
                           │   │
       (SALE deposit)      │   └──(admin complete)──> COMPLETED
           │               │
           v               │
     DEPOSIT_PENDING ─(approve)──> DEPOSITED ──(admin cancel)──> AVAILABLE
       │  │  │                │        │    │
       │  │  │ (reject)       │        │    └──(admin soldout)──> SOLDOUT
       │  │  └──> AVAILABLE   │        │
       │  │                   │        └──(admin complete)──> COMPLETED
       │  └──(SALE soldout)──> SOLDOUT_PENDING ─(approve)──> SOLDOUT
       │                            │ (reject)
       │                            └──> DEPOSITED
       └──(SALE cancel)──> CANCEL_PENDING ─(approve)──> AVAILABLE
       │                       │ (reject)
       │                       └──> DEPOSITED
       └──(SALE complete)──> COMPLETE_PENDING ─(approve)──> COMPLETED
                               │ (reject)
                               └──> DEPOSITED

  SOLDOUT ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
  EXPIRED ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
  COMPLETED ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
```

### Pending statuses requiring approval
`POST_PENDING`, `EDIT_PENDING`, `DEPOSIT_PENDING`, `SOLDOUT_PENDING`, `COMPLETE_PENDING`, `CANCEL_PENDING`, `REOPEN_PENDING`

### Terminal statuses
`DEPOSITED`, `SOLDOUT`, `EXPIRED`, `COMPLETED`

### SALE vs ADMIN/APPROVER behavior
| Action | SALE | ADMIN/APPROVER |
|---|---|---|
| Submit draft | → POST_PENDING + approval + notification | → AVAILABLE directly |
| Deposit | → DEPOSIT_PENDING + approval + notification | → DEPOSITED directly |
| Soldout | → SOLDOUT_PENDING + approval + notification | → SOLDOUT directly |
| Cancel | → CANCEL_PENDING + approval + notification | → AVAILABLE directly |
| Complete | → COMPLETE_PENDING + approval + notification | → COMPLETED directly |
| Reopen | → REOPEN_PENDING + approval + notification | → AVAILABLE directly |
| Edit (available) | → EDIT_PENDING + approval + notification | Changes applied immediately |
| Withdraw | → Reverts to previous status | Not needed |

### Withdraw revert mapping
| From Status | Returns To |
|---|---|
| POST_PENDING | DRAFT |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | from_property_status (stored in approval) |

---

## Cross-Domain Interaction Map

```
Properties ──creates──> Approvals ──decides──> Properties (status change)
     │                      │
     │                      └──notifies──> Notifications ──WebSocket──> Client
     │
     ├──creates──> Transitions (status logs)
     │
     ├──owns──> Reviews ──has──> Files
     │
     ├──has──> Pins (per user)
     │
     ├──has──> Hot Properties (admin-managed)
     │
     └──uses──> Tags, Transaction Types, Property Types

Auth ──creates──> Users ──belongs_to──> Organizations
     │
     ├──manages──> Refresh Tokens (rotation)
     │
     ├──manages──> Token Blacklist (logout)
     │
     └──enforces──> Device Limit (SALE/APPROVER only)

Files ──uploaded_by──> Users
     │
     ├──optimized_to──> WebP (+ thumbnails)
     │
     ├──trashed_on_delete──> Cleanup (30-day retention)
     │
     └──linked_to──> Properties, Reviews, Avatars, Certificates

Notifications ──created_by──> Property state changes
     │
     └──sent_via──> WebSocket (real-time)

Carts ──counts──> Properties (per-user status breakdown)
Expirations ──auto-expires──> Deposited/Deposit-pending properties
Backfills ──rebuilds──> Search text index
```

---

## Domain Files

| File | Domain | Key Endpoints |
|---|---|---|
| [types.md](./types.md) | All types | Enums, entities, request/response schemas |
| [auth.md](./auth.md) | Auth + Profile | Login, refresh, logout, password, profile |
| [properties.md](./properties.md) | Properties | CRUD, transitions, state machine, status-logs |
| [approvals.md](./approvals.md) | Approvals | List, approve, reject, counts |
| [users.md](./users.md) | Users | Admin CRUD, deactivate, reset-password |
| [organizations.md](./organizations.md) | Organizations | CRUD with active-user constraint |
| [files.md](./files.md) | Files | Upload, delete, optimization, cleanup |
| [reviews.md](./reviews.md) | Reviews | CRUD per property |
| [notifications.md](./notifications.md) | Notifications | List, read, counts, preferences |
| [meta-data.md](./meta-data.md) | Meta Data | Transaction types, Property types, Tags |
| [assets.md](./assets.md) | Assets | Pins, Hot properties, My assets, Carts |
| [system.md](./system.md) | System | Geography, Master data, Supports, Backfills, WebSocket |
