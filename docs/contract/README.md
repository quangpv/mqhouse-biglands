# API Contract

Business rules for all Biglands APIs, organized by domain.

## Global Rules

### Authentication
- Every action requires a signed-in session unless the endpoint is marked **Public**.
- A signed-in session lasts 24 hours. Users are automatically re-authenticated if they have an active refresh session (valid 7 days).
- Each refresh session can only be used once. A new one is issued automatically after each refresh.
- Signing out cancels the current session and all other active sessions for that user.

### Authorization
- Three roles exist: **Sales**, **Approver**, and **Admin**.
- Actions are restricted by role. If a user's role is not in the allowed list, the action is denied.
- Deactivated users cannot access any action that requires a signed-in session.

### Error Responses
| Situation | What Happens |
|---|---|
| Resource not found | 404 — The requested item does not exist |
| Conflict with existing data | 409 — The request conflicts with current state |
| Invalid request | 400 — The request is malformed or missing required data |
| Not signed in | 401 — Authentication required |
| Not authorized | 403 — You do not have permission for this action |

### Pagination
- Lists return up to 20 items per page by default (maximum 100).
- Each response includes total items and total pages for navigation.

### Phone Number Privacy
- Creator phone number is visible to all authenticated users.
- House holder phone number is visible only to: the property creator, admins, and approvers.
- Sales staff who are not the creator cannot see the house holder phone number.

### Auto-Rejection Cascade
- When any user acts on a property that already has a pending approval, the existing approval is automatically rejected.
- This applies to all status transitions (deposit, sold out, cancel, complete, reopen) and edits.
- The auto-rejected approval is recorded as rejected in the approval history.

### Organization-Scoped Notifications
- When a Sales staff member submits a property for approval, only admins and approvers within the same organization are notified.
- This ensures notifications are relevant to the user's team.

### File Content Hashing
- Each uploaded file gets a SHA-256 content hash stored for deduplication and integrity verification.

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
                          (Admin/Approver publish)
DRAFT ──────────────────────────────────────────────> AVAILABLE
  │                                                       │
  │ (Sales submit for approval)                            │
  └──────────────> POST_PENDING ──(approve)───────────────┘
                         │         (reject)
                         │            │
                         │            └──> DRAFT
                         │ (Sales withdraw)
                         └──> DRAFT

                         AVAILABLE ──(admin soldout)──> SOLDOUT
                           │   │
       (Sales deposit)     │   └──(admin complete)──> COMPLETED
           │               │
           v               │
     DEPOSIT_PENDING ─(approve)──> DEPOSITED ──(admin cancel)──> AVAILABLE
       │  │  │                │        │    │
       │  │  │ (reject)       │        │    └──(admin soldout)──> SOLDOUT
       │  │  └──> AVAILABLE   │        │
       │  │                   │        └──(admin complete)──> COMPLETED
       │  └──(Sales soldout)──> SOLDOUT_PENDING ─(approve)──> SOLDOUT
       │                            │ (reject)
       │                            └──> DEPOSITED
       └──(Sales cancel)──> CANCEL_PENDING ─(approve)──> AVAILABLE
       │                       │ (reject)
       │                       └──> DEPOSITED
       └──(Sales complete)──> COMPLETE_PENDING ─(approve)──> COMPLETED
                               │ (reject)
                               └──> DEPOSITED

  SOLDOUT ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
  EXPIRED ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
  COMPLETED ──(reopen)──> REOPEN_PENDING ──(approve)──> AVAILABLE
```

### Expiration trigger (midnight cron)
- **DEPOSITED** → EXPIRED (if contract date is strictly before today)
- **DEPOSIT_PENDING** → rejected, rolls back to previous status (if contract date is strictly before today)

### Pending statuses requiring approval
The following statuses indicate a request is waiting for approval: `POST_PENDING`, `EDIT_PENDING`, `DEPOSIT_PENDING`, `SOLDOUT_PENDING`, `COMPLETE_PENDING`, `CANCEL_PENDING`, `REOPEN_PENDING`

### Terminal statuses
The following statuses are final and cannot be changed directly: `DEPOSITED`, `SOLDOUT`, `EXPIRED`, `COMPLETED`

### SALE vs ADMIN/APPROVER behavior
| Action | Sales Staff | Admin / Approver |
|---|---|---|
| Submit draft | Goes to approval queue; admins/approvers notified | Published immediately |
| Deposit | Goes to approval queue; admins/approvers notified | Confirmed immediately |
| Sold out | Goes to approval queue; admins/approvers notified | Confirmed immediately |
| Cancel | Goes to approval queue; admins/approvers notified | Cancelled immediately |
| Complete | Goes to approval queue; admins/approvers notified | Completed immediately |
| Reopen | Goes to approval queue; admins/approvers notified | Reopened immediately |
| Edit (available listing) | Goes to approval queue; admins/approvers notified | Changes applied immediately |
| Withdraw | Reverts to previous status | Not applicable |

### Withdraw revert mapping
| From Status | Returns To |
|---|---|
| POST_PENDING | DRAFT |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | Status before the original request |

---

## Cross-Domain Interaction Map

```
Properties ──triggers──> Approvals ──decides──> Properties (status change)
     │                      │
     │                      └──sends──> Notifications ──WebSocket──> Client
     │
     ├──records──> Status History (transitions)
     │
     ├──has──> Reviews ──may include──> Files
     │
     ├──may be──> Pinned (per user)
     │
     ├──may be──> Hot Properties (admin-managed)
     │
     └──categorized by──> Tags, Transaction Types, Property Types

Auth ──creates──> Users ──belong to──> Organizations
     │
     ├──manages──> Active Sessions (rotation)
     │
     ├──manages──> Signed-out Sessions (blacklist)
     │
     └──enforces──> Device Limit (Sales and Approvers only)

Files ──uploaded by──> Users
     │
     ├──optimized to──> WebP (+ thumbnails)
     │
     ├──moved to trash on delete──> Cleanup (30-day retention)
     │
     └──linked to──> Properties, Reviews, Avatars, Certificates

Notifications ──created by──> Property state changes
     │
     └──delivered via──> WebSocket (real-time)

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
