# Architecture — Biglands Backend

> **Skill**: `backend-patterns` — Async-FastAPI + SQLAlchemy, facade-per-use-case  
> **Source Documents**: domain-model.md, openapi.yaml  
> **Status**: Design reference — no implementation

---

## 1. Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Runtime | Python | 3.10+ |
| Framework | FastAPI | latest |
| ORM | SQLAlchemy (async) | 2.x |
| DB Driver | asyncpg | latest |
| Migrations | Alembic | latest |
| Validation | Pydantic | v2 |
| Auth | JWT (python-jose) + bcrypt | — |
| Background | asyncio.Queue via BackgroundExecutor | — |
| Scheduler | APScheduler | latest |
| Container | Custom DI (inspect-based) | — |
| DB | PostgreSQL | 16 |

---

## 2. Project Structure

```
src/
├── __init__.py
├── main.py                              # App entry: load_modules() → FastAPI
│
├── platform/
│   ├── __init__.py
│   ├── config.py                        # Pydantic BaseSettings (env vars)
│   ├── container.py                     # DI container (inspect-based)
│   ├── database.py                      # async_session_factory, get_session
│   ├── auth.py                          # get_current_user, require_role deps
│   ├── security.py                      # hash_password, verify, JWT create/decode
│   ├── dependencies.py                  # get_db, get_executor, get_scheduler
│   ├── logger.py                        # AppLogger — console + file
│   ├── background.py                    # BackgroundExecutor (asyncio queue)
│   └── scheduler.py                     # AppScheduler (APScheduler + lifespan)
│
├── data/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py                  # Re-exports all entities
│   │   ├── _base.py                     # DeclarativeBase + common mixins
│   │   ├── user.py                      # UserEntity
│   │   ├── listing.py                   # ListingEntity
│   │   ├── listing_image.py             # ListingImageEntity
│   │   ├── deal_event.py               # DealEventEntity
│   │   ├── approval.py                  # ApprovalEntity
│   │   ├── notification.py             # NotificationEntity
│   │   ├── user_pin.py                 # UserPinEntity (proposed)
│   │   └── review.py                        # ReviewEntity
│   └── repositories/
│       ├── __init__.py                  # Re-exports all repos
│       ├── user_repo.py                 # UserRepo
│       ├── listing_repo.py              # ListingRepo
│       ├── listing_image_repo.py        # ListingImageRepo
│       ├── deal_event_repo.py           # DealEventRepo
│       ├── approval_repo.py             # ApprovalRepo
│       ├── notification_repo.py         # NotificationRepo
│       ├── user_pin_repo.py             # UserPinRepo (proposed)
│       └── review_repo.py               # ReviewRepo
│
├── modules/
│   ├── __init__.py
│   │
│   ├── auth/                            # POST /login, POST /logout, GET /me, forgot/reset password
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── login.py
│   │       ├── logout.py
│   │       ├── get_current_user.py
│   │       ├── forgot_password.py
│   │       └── reset_password.py
│   │
│   ├── users/                           # CRUD + deactivate + reactivate + role
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── create_user.py
│   │       ├── list_users.py
│   │       ├── get_user.py
│   │       ├── update_user.py
│   │       ├── deactivate_user.py
│   │       ├── reactivate_user.py
│   │       └── assign_role.py
│   │
│   ├── listings/                        # CRUD + submit + withdraw + browse
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── create_listing.py
│   │       ├── list_listings.py
│   │       ├── get_listing.py
│   │       ├── update_listing.py
│   │       ├── delete_listing.py
│   │       ├── submit_listing.py
│   │       └── withdraw_listing.py
│   │
│   ├── listing_images/                  # Upload / delete / reorder / set-primary
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── upload_image.py
│   │       ├── delete_image.py
│   │       ├── set_primary_image.py
│   │       └── reorder_images.py
│   │
│   ├── deal_events/                     # Report deposit/closure/cancellation/sold-out
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── report_deposit.py
│   │       ├── report_closure.py
│   │       ├── report_cancellation.py
│   │       └── report_sold_out.py
│   │
│   ├── approvals/                       # Queues + approve + reject + bulk
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── list_queues.py
│   │       ├── list_queue_items.py
│   │       ├── get_approval.py
│   │       ├── approve_item.py
│   │       ├── reject_item.py
│   │       └── bulk_approve.py
│   │
│   ├── notifications/                   # List + mark read + read-all + count
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── list_notifications.py
│   │       ├── get_unread_count.py
│   │       ├── mark_read.py
│   │       └── mark_all_read.py
│   │
│   ├── hot_products/                    # Promote + unpromote + list + reorder
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── promote_to_hot.py
│   │       ├── unpromote_from_hot.py
│   │       ├── get_hot_listings.py
│   │       └── reorder_hot_listings.py
│   │
│   ├── pins/                            # Pin / unpin / list-my-pins
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── mapper.py
│   │   └── facades/
│   │       ├── __init__.py
│   │       ├── pin_listing.py
│   │       ├── unpin_listing.py
│   │       └── list_my_pins.py
│   │
│   └── user_settings/                   # Notification preferences
│       ├── __init__.py
│       ├── router.py
│       ├── schemas.py
│       ├── mapper.py
│       └── facades/
│           ├── __init__.py
│           ├── get_notification_preferences.py
│           └── update_notification_preferences.py
│
└── shared/
    ├── __init__.py
    ├── errors/
    │   ├── __init__.py
    │   └── exceptions.py                # NotFoundError, ConflictError, BadRequestError, ForbiddenError
    ├── pagination/
    │   └── __init__.py                  # PaginationParams, PaginatedResponse, paginate()
    └── utils/
        └── __init__.py                  # code_generator, status_machine helpers
```

---

## 3. Module Breakdown

### 3.1 Module Inventory

| Module | Prefix | Auth Required | Min Role | # Endpoints |
|--------|--------|---------------|----------|-------------|
| `auth` | `/auth` | Mixed (login=public) | — | 5 |
| `users` | `/users` | Yes | ADMIN | 8 |
| `listings` | `/listings` | Yes | AGENT | 7 |
| `listing_images` | `/listings/{id}/images` | Yes | AGENT | 4 |
| `deal_events` | `/listings/{id}/deal-events` | Yes | AGENT | 4 |
| `approvals` | `/approvals` | Yes | APPROVER | 6 |
| `notifications` | `/notifications` | Yes | AGENT | 4 |
| `hot_products` | `/hot-listings` + `/listings/{id}/promote` | Yes | ADMIN (mutate) | 4 |
| `pins` | `/listings/{id}/pin` + `/users/me/pins` | Yes | AGENT | 3 |
| `user_settings` | `/users/me/notification-preferences` | Yes | AGENT | 2 |

### 3.2 Router → Facade → Repository Mapping

| Method | Path | Facade | Repo | Entity |
|--------|------|--------|------|--------|
| `POST` | `/auth/login` | `login` | `UserRepo` | User |
| `POST` | `/auth/logout` | `logout` | — | — |
| `GET` | `/auth/me` | `get_current_user` | `UserRepo` | User |
| `POST` | `/auth/forgot-password` | `forgot_password` | `UserRepo` | User |
| `POST` | `/auth/reset-password` | `reset_password` | `UserRepo` | User |
| `POST` | `/users` | `create_user` | `UserRepo` | User |
| `GET` | `/users` | `list_users` | `UserRepo` | User |
| `GET` | `/users/{id}` | `get_user` | `UserRepo` | User |
| `PUT` | `/users/{id}` | `update_user` | `UserRepo` | User |
| `PATCH` | `/users/{id}/deactivate` | `deactivate_user` | `UserRepo` | User |
| `PATCH` | `/users/{id}/reactivate` | `reactivate_user` | `UserRepo` | User |
| `PATCH` | `/users/{id}/role` | `assign_role` | `UserRepo` | User |
| `POST` | `/listings` | `create_listing` | `ListingRepo`, `ListingImageRepo` | Listing, ListingImage |
| `GET` | `/listings` | `list_listings` | `ListingRepo`, `UserPinRepo` | Listing, UserPin |
| `GET` | `/listings/{id}` | `get_listing` | `ListingRepo`, `ListingImageRepo`, `DealEventRepo` | Listing, ListingImage, DealEvent |
| `PUT` | `/listings/{id}` | `update_listing` | `ListingRepo` | Listing |
| `DELETE` | `/listings/{id}` | `delete_listing` | `ListingRepo` | Listing |
| `POST` | `/listings/{id}/submit` | `submit_listing` | `ListingRepo`, `ListingImageRepo` | Listing, ListingImage |
| `POST` | `/listings/{id}/withdraw` | `withdraw_listing` | `ListingRepo` | Listing |
| `POST` | `/listings/{id}/images` | `upload_image` | `ListingImageRepo` | ListingImage |
| `PUT` | `/listings/{id}/images/reorder` | `reorder_images` | `ListingImageRepo` | ListingImage |
| `DELETE` | `/listings/{listingId}/images/{imageId}` | `delete_image` | `ListingImageRepo` | ListingImage |
| `PUT` | `/listings/{listingId}/images/{imageId}/primary` | `set_primary_image` | `ListingImageRepo` | ListingImage |
| `POST` | `/listings/{id}/deal-events/deposit` | `report_deposit` | `DealEventRepo`, `ListingRepo` | DealEvent, Listing |
| `POST` | `/listings/{id}/deal-events/closure` | `report_closure` | `DealEventRepo`, `ListingRepo` | DealEvent, Listing |
| `POST` | `/listings/{id}/deal-events/cancellation` | `report_cancellation` | `DealEventRepo`, `ListingRepo` | DealEvent, Listing |
| `POST` | `/listings/{id}/deal-events/sold-out` | `report_sold_out` | `DealEventRepo`, `ListingRepo` | DealEvent, Listing |
| `GET` | `/approvals/queues` | `list_queues` | `ApprovalRepo` | Approval |
| `GET` | `/approvals/queues/{queueType}` | `list_queue_items` | `ApprovalRepo`, `DealEventRepo` | Approval, Listing, DealEvent |
| `GET` | `/approvals/{id}` | `get_approval` | `ApprovalRepo` | Approval |
| `POST` | `/approvals/{id}/approve` | `approve_item` | `ApprovalRepo`, `ListingRepo`, `DealEventRepo` | Approval, Listing, DealEvent |
| `POST` | `/approvals/{id}/reject` | `reject_item` | `ApprovalRepo`, `ListingRepo` | Approval, Listing |
| `POST` | `/approvals/bulk-approve` | `bulk_approve` | `ApprovalRepo`, `ListingRepo` | Approval, Listing |
| `GET` | `/notifications` | `list_notifications` | `NotificationRepo` | Notification |
| `GET` | `/notifications/unread-count` | `get_unread_count` | `NotificationRepo` | Notification |
| `PATCH` | `/notifications/{id}/read` | `mark_read` | `NotificationRepo` | Notification |
| `POST` | `/notifications/read-all` | `mark_all_read` | `NotificationRepo` | Notification |
| `POST` | `/listings/{id}/promote` | `promote_to_hot` | `ListingRepo` | Listing |
| `DELETE` | `/listings/{id}/promote` | `unpromote_from_hot` | `ListingRepo` | Listing |
| `GET` | `/hot-listings` | `get_hot_listings` | `ListingRepo` | Listing |
| `PUT` | `/hot-listings/reorder` | `reorder_hot_listings` | `ListingRepo` | Listing |
| `PUT` | `/listings/{id}/pin` | `pin_listing` | `UserPinRepo` | UserPin |
| `DELETE` | `/listings/{id}/pin` | `unpin_listing` | `UserPinRepo` | UserPin |
| `GET` | `/users/me/pins` | `list_my_pins` | `UserPinRepo`, `ListingRepo` | UserPin, Listing |
| `GET` | `/users/me/notification-preferences` | `get_notification_preferences` | `UserRepo` | User (prefs) |
| `PUT` | `/users/me/notification-preferences` | `update_notification_preferences` | `UserRepo` | User (prefs) |

---

## 4. Entity Definitions

All entities follow SQLAlchemy 2.x `Mapped` style per skill convention.

### 4.1 Naming Conventions

| Rule | Value |
|------|-------|
| `__tablename__` | Plural snake_case: `users`, `listings`, `listing_images` |
| PK type | `UUID(as_uuid=True)` with `default=uuid.uuid4` |
| Timestamps | `DateTime(timezone=True)` with `server_default=func.now()` |
| FK naming | `<entity>_id` (e.g., `created_by_id`, `listing_id`) |
| Enum storage | `sa.Enum(...)` or `sa.String()` for PG-compatible enum |

### 4.2 Entity Relationship Map

```
UserEntity
├── id (PK, UUID)
├── full_name (String 255, required)
├── username (String 100, required, unique)
├── phone (String 20, nullable)
├── email (String 255, nullable)
├── password_hash (String 255, required)
├── role (Enum: AGENT|APPROVER|ADMIN, default AGENT)
├── is_active (Boolean, default true)
├── notification_prefs (JSONB, nullable)        ← stores NotificationPreferences shape
├── created_by_id (FK → User.id, nullable)
├── created_at (DateTime, server_default)
└── updated_at (DateTime, onupdate)

Relationships:
  User "creates" Listing           → 1:N (onDelete: RESTRICT)
  User "reports" DealEvent         → 1:N (onDelete: RESTRICT)
  User "decides" Approval          → 1:N (onDelete: RESTRICT)
  User "receives" Notification     → 1:N (onDelete: CASCADE)
  User "pins" Listing              → N:M via UserPin (onDelete: CASCADE)
  User "created by" User           → N:1 self-ref (onDelete: SET NULL)
```

```
ListingEntity
├── id (PK, UUID)
├── code (String 20, required, unique)
├── transaction_type (Enum: SANG_NHUONG|CHO_THUE|BAN)
├── title (String 500, nullable)
├── description (Text, required)
├── price (Numeric 18,0, required)
├── commission_type (Enum: PERCENTAGE|FLAT)
├── commission_value (Numeric 18,0)
├── area_width (Numeric 10,2)
├── area_length (Numeric 10,2)
├── total_area (Numeric 10,2)
├── num_rooms (Integer, default 0)
├── num_bathrooms (Integer, default 0)
├── num_floors (Integer, default 0)
├── street_name (String 255)
├── house_number (String 50)
├── address (String 500)
├── ward (String 100)
├── district (String 100)
├── city (String 100, default "Hồ Chí Minh")
├── latitude (Numeric 10,8, nullable)
├── longitude (Numeric 11,8, nullable)
├── label (String 100, nullable)
├── furnishing (String 500, nullable)
├── frontage_type (String 100, nullable)
├── legal_status (String 500, nullable)
├── direction (String 50, nullable)
├── road_width (String 50, nullable)
├── owner_phone (String 20)
├── video_url (String 500, nullable)
├── status (Enum: DRAFT|PENDING_APPROVAL|CON_HANG|DA_COC|HET_HANG|DA_CHOT|HUY_COC|QUA_HAN, default DRAFT)
├── is_hot (Boolean, default false)
├── hot_order (Integer, nullable, unique among hot items)
├── view_count (Integer, default 0)
├── created_by_id (FK → User.id, required)
├── approved_by_id (FK → User.id, nullable)
├── approved_at (DateTime, nullable)
├── created_at (DateTime, server_default)
└── updated_at (DateTime, onupdate)

Relationships:
  Listing "has" ListingImage       → 1:N (onDelete: CASCADE)
  Listing "tracks" DealEvent       → 1:N (onDelete: CASCADE)
  Listing "requires" Approval      → 1:N (onDelete: CASCADE)
  Listing "pinned by" User         → N:M via UserPin (onDelete: CASCADE)
```

```
ListingImageEntity
├── id (PK, UUID)
├── listing_id (FK → Listing.id, required)
├── url (String 1000, required)
├── order (Integer, default 0)
└── is_primary (Boolean, default false)

Constraints:
  UNIQUE(listing_id, order)
  MAX 20 images per listing_id
  At most one is_primary = true per listing_id
```

```
DealEventEntity
├── id (PK, UUID)
├── listing_id (FK → Listing.id, required)
├── event_type (Enum: DEPOSIT_REPORTED|DEPOSIT_CONFIRMED|CLOSURE_REPORTED|CLOSURE_CONFIRMED|CANCELLATION_REPORTED|CANCELLATION_CONFIRMED|SOLD_OUT_REPORTED|SOLD_OUT_CONFIRMED)
├── reported_by_id (FK → User.id, required)
├── confirmed_by_id (FK → User.id, nullable)
├── confirmed_at (DateTime, nullable)
├── notes (Text, nullable)
├── customer_name (String 255, nullable)
├── customer_phone (String 20, nullable)
├── deposit_amount (Numeric 18,0, nullable)
└── created_at (DateTime, server_default)

Invariants (enforced via facade logic):
  DEPOSIT_REPORTED requires customer_name + deposit_amount > 0
  CANCELLATION_REPORTED requires notes
  Immutable after creation
```

```
ApprovalEntity
├── id (PK, UUID)
├── listing_id (FK → Listing.id, required)
├── approval_type (Enum: LISTING_POST|DEPOSIT|CANCELLATION|CLOSURE|SOLD_OUT)
├── decision (Enum: APPROVED|REJECTED)
├── decided_by_id (FK → User.id, required)
├── reason (Text, nullable)                     ← required when REJECTED
└── created_at (DateTime, server_default)

Constraints:
  UNIQUE(listing_id, approval_type) for concurrency guard
```

```
NotificationEntity
├── id (PK, UUID)
├── user_id (FK → User.id, required)
├── title (String 500)
├── body (Text)
├── reference_type (Enum: LISTING|APPROVAL|DEAL_EVENT, nullable)
├── reference_id (UUID, nullable)
├── is_read (Boolean, default false)
├── event_type (String 100, nullable)         ← structured: "listing_submitted", "deposit_confirmed", etc.
├── actor_name (String 255, nullable)         ← display name of the triggering user
├── transaction_type (String 50, nullable)    ← "BAN", "CHO_THUE", "SANG_NHUONG"
└── created_at (DateTime, server_default)

Index: (user_id, is_read, created_at DESC)
```

```
UserPinEntity  (proposed — see domain-model.md §7)
├── user_id (FK → User.id, PK composite)
├── listing_id (FK → Listing.id, PK composite)
└── pinned_at (DateTime, server_default)

Constraints:
  Composite PK prevents duplicates (CPK)
```

```
ReviewEntity  (implemented — see domain-model.md §8)
├── id (PK, UUID)
├── listing_id (FK → Listing.id)
├── user_id (FK → User.id)
├── content (Text, required)
├── rating (Integer, nullable)
├── is_moderated (Boolean, default false)
└── created_at (DateTime, server_default)
```

---

## 5. Repository Pattern

### 5.1 Standard Methods

Every repo provides these methods:

```python
class SomeRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, id: UUID) -> Entity | None
    async def list(self, *, page: int = 1, size: int = 20, **filters) -> tuple[list[Entity], int]
    async def create(self, entity: Entity) -> Entity
    async def update(self, entity: Entity) -> Entity
    async def delete(self, entity: Entity) -> None
```

### 5.2 Per-Entity Repo Specializations

| Repo | Entity | Special Methods |
|------|--------|----------------|
| `UserRepo` | User | `get_by_username()`, `count_active_admins()`, `list_by_ids()` |
| `ListingRepo` | Listing | `get_by_code()`, `list_hot()`, `count_active()`, `increment_view_count()`, `list_expired()` |
| `ListingImageRepo` | ListingImage | `count_by_listing()`, `set_primary()` |
| `DealEventRepo` | DealEvent | `get_pending_confirmation()`, `has_active_deposit()`, `get_by_listing()` |
| `ApprovalRepo` | Approval | `get_queue_counts()`, `list_queue_items()`, `get_by_listing_and_type()`, `count_pending()` |
| `NotificationRepo` | Notification | `get_unread_count()`, `mark_all_read()`, `list_by_user()`, `get_category_counts()` |
| `UserPinRepo` | UserPin | `get_by_user_and_listing()`, `list_by_user()` |

---

## 6. Facade Pattern

### 6.1 Contract

Every facade is a single async function exported from its own file:

```python
async def <verb>_<noun>(
    data: <RequestSchema> = Depends(),
    repo: <Entity>Repo = Depends(<Entity>Repo),
    current_user: UserEntity = Depends(get_current_user),
    executor: BackgroundExecutor = Depends(get_executor),
) -> <ResponseSchema>
```

- **Input**: Pydantic request schema via `Depends()`
- **Dependencies**: Repos, services, current_user via `Depends()`
- **Output**: Pydantic response schema (never a raw entity)
- **Errors**: Raise typed exceptions (`NotFoundError`, `ConflictError`, `BadRequestError`, `ForbiddenError`)
- **Side effects**: Logger calls, background task enqueues

### 6.2 Listing Status Machine Enforcement

Each mutating facade validates the status transition against the state diagram. Invalid transitions raise `ConflictError` with code `INVALID_STATUS_TRANSITION`.

```python
# Valid transition map (defined in shared/utils/status_machine.py)
STATUS_TRANSITIONS: dict[ListingStatus, set[ListingStatus]] = {
    ListingStatus.DRAFT:               {PENDING_APPROVAL, DELETED},
    ListingStatus.PENDING_APPROVAL:    {CON_HANG, DRAFT, QUA_HAN},
    ListingStatus.CON_HANG:           {DA_COC, HET_HANG, DRAFT, QUA_HAN},
    ListingStatus.DA_COC:             {DA_CHOT, HUY_COC},
    # Terminal states: HET_HANG, DA_CHOT, HUY_COC, QUA_HAN → no outgoing
}
```

### 6.3 Example: `create_listing` Facade

```python
async def create_listing(
    data: CreateListingRequest = Depends(),
    listing_repo: ListingRepo = Depends(ListingRepo),
    current_user: UserEntity = Depends(get_current_user),
    executor: BackgroundExecutor = Depends(get_executor),
) -> ListingResponse:

    if not current_user.is_active:
        raise ForbiddenError("Account is deactivated")

    listing = build_listing_entity(data, created_by_id=current_user.id)

    if data.action == "submit":
        listing.status = ListingStatus.PENDING_APPROVAL
        # ── note: image count validated in submit_listing facade ──
    else:
        listing.status = ListingStatus.DRAFT

    if current_user.role == UserRole.ADMIN:
        listing.status = ListingStatus.CON_HANG
        listing.approved_by_id = current_user.id
        listing.approved_at = datetime.now(timezone.utc)

    listing = await listing_repo.create(listing)
    logger.info("Created listing %s (user=%s)", listing.id, current_user.id)

    if listing.status == ListingStatus.PENDING_APPROVAL:
        executor.enqueue(notify_approvers, listing_id=listing.id)

    return listing_to_response(listing)
```

### 6.4 Example: `approve_item` Facade

```python
async def approve_item(
    approval_id: UUID = ...,
    approval_repo: ApprovalRepo = Depends(ApprovalRepo),
    listing_repo: ListingRepo = Depends(ListingRepo),
    deal_event_repo: DealEventRepo = Depends(DealEventRepo),
    current_user: UserEntity = Depends(get_current_user),
    executor: BackgroundExecutor = Depends(get_executor),
) -> ApprovalResponse:

    # 1. Fetch with pessimistic lock
    approval = await approval_repo.get_for_update(approval_id)
    if approval is None:
        raise NotFoundError("Approval not found")
    if approval.decision is not None:
        raise ConflictError("Already processed")

    # 2. Fetch listing and validate state
    listing = await listing_repo.get(approval.listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    validate_approval_type_status(approval.approval_type, listing.status)

    # 3. Apply decision
    approval.decision = Decision.APPROVED
    approval.decided_by_id = current_user.id
    new_status = APPROVED_STATUS_MAP[approval.approval_type]

    if approval.approval_type == ApprovalType.DEPOSIT:
        deal_event = await deal_event_repo.get_pending_deposit(listing.id)
        deal_event.confirmed_by_id = current_user.id
        deal_event.confirmed_at = datetime.now(timezone.utc)

    listing.status = new_status
    listing.approved_by_id = current_user.id
    listing.approved_at = datetime.now(timezone.utc)

    await approval_repo.update(approval)
    await listing_repo.update(listing)

    # 4. Notify agent
    executor.enqueue(notify_listing_approved, listing_id=listing.id)

    return approval_to_response(approval)
```

---

## 7. Notification System

### 7.1 Architecture

```
Facade (business logic)
    │
    ├── executor.enqueue(notify_xxx, listing_id=...)
    │
    ▼
BackgroundExecutor (asyncio.Queue)
    │
    ├── worker loop: dequeue → send_notification()
    │       ├── check user preferences
    │       ├── create NotificationEntity
    │       └── NotificationRepo.create()
    │
    └── retry 3x on failure, then log and skip
```

### 7.2 Trigger → Notification Mapping

| Trigger Event | Notification Facade | Recipient |
|--------------|---------------------|-----------|
| Listing submitted | `notify_listing_submitted` | All APPROVERs |
| Listing approved | `notify_listing_approved` | Agent (listing creator) |
| Listing rejected | `notify_listing_rejected` | Agent (listing creator) |
| Deposit reported | `notify_deposit_reported` | All APPROVERs |
| Deposit confirmed | `notify_deposit_confirmed` | Agent (reporter) |
| Deposit rejected | `notify_deposit_rejected` | Agent (reporter) |
| Closure reported | `notify_closure_reported` | All APPROVERs |
| Closure confirmed | `notify_closure_confirmed` | Agent (reporter) |
| Closure rejected | `notify_closure_rejected` | Agent (reporter) |
| Cancellation reported | `notify_cancellation_reported` | All APPROVERs |
| Cancellation confirmed | `notify_cancellation_confirmed` | Agent (reporter) |
| Cancellation rejected | `notify_cancellation_rejected` | Agent (reporter) |
| Sold-out reported | `notify_sold_out_reported` | All APPROVERs |
| Sold-out confirmed | `notify_sold_out_confirmed` | Agent (reporter) |
| Sold-out rejected | `notify_sold_out_rejected` | Agent (reporter) |
| Listing expired | `notify_listing_expired` | Agent (listing creator) |

### 7.3 Preference Filtering

Each notification facade checks the user's `notification_prefs` before creating a record:

```python
async def send_notification(user_id: UUID, event_type: str, title: str, body: str):
    user = await user_repo.get(user_id)
    if user is None:
        return
    prefs = user.notification_prefs or DEFAULT_PREFS
    if not prefs.get(event_type, True):
        return  # user disabled this type
    notification = NotificationEntity(
        user_id=user_id, title=title, body=body,
        reference_type=..., reference_id=...
    )
    await notification_repo.create(notification)
```

---

## 8. Key Algorithms

### 8.1 Product Code Generation

Format: `YYMMDD` + 7 random digits (e.g., `2505202605828`)

```python
def generate_product_code() -> str:
    date_part = datetime.now(timezone.utc).strftime("%y%m%d")
    random_part = str(random.randint(1000000, 9999999))
    return f"{date_part}{random_part}"[:20]
```

### 8.2 Listing Status Machine

```python
STATUS_TRANSITIONS: dict[ListingStatus, set[ListingStatus]] = {
    ListingStatus.DRAFT:               {ListingStatus.PENDING_APPROVAL},
    ListingStatus.PENDING_APPROVAL:    {ListingStatus.CON_HANG, ListingStatus.DRAFT, ListingStatus.QUA_HAN},
    ListingStatus.CON_HANG:           {ListingStatus.DA_COC, ListingStatus.HET_HANG, ListingStatus.DRAFT, ListingStatus.QUA_HAN},
    ListingStatus.DA_COC:             {ListingStatus.DA_CHOT, ListingStatus.HUY_COC},
    ListingStatus.HET_HANG:           set(),   # terminal
    ListingStatus.DA_CHOT:            set(),   # terminal
    ListingStatus.HUY_COC:            set(),   # terminal
    ListingStatus.QUA_HAN:            set(),   # terminal
}

def validate_transition(current: ListingStatus, next_: ListingStatus):
    if next_ not in STATUS_TRANSITIONS.get(current, set()):
        raise ConflictError(
            code="INVALID_STATUS_TRANSITION",
            message=f"Cannot transition from {current} to {next_}"
        )
```

### 8.3 Re-Approval Trigger Detection

```python
REAPPROVAL_FIELDS = {"price", "area_width", "area_length", "total_area"}

def requires_reapproval(old: ListingEntity, update: dict) -> bool:
    if old.status != ListingStatus.CON_HANG:
        return False
    return any(field in update for field in REAPPROVAL_FIELDS)
```

Used in `update_listing` facade:

```python
changes = extract_changes(existing, data)
if requires_reapproval(existing, changes):
    existing.status = ListingStatus.PENDING_APPROVAL
```

### 8.4 Expired Listing Scheduler

Cron job runs hourly via `AppScheduler` (APScheduler):

```python
async def expire_listings():
    cutoff = datetime.now(timezone.utc) - timedelta(days=EXPIRATION_DAYS)
    expired = await listing_repo.list_expired(cutoff)
    for listing in expired:
        listing.status = ListingStatus.QUA_HAN
        await listing_repo.update(listing)
        executor.enqueue(notify_listing_expired, listing_id=listing.id)
```

| Config | Default | Source |
|--------|---------|--------|
| `EXPIRATION_DAYS` | 30 | MR-03 (to be confirmed) |

---

## 9. Error Handling

### 9.1 Exception Classes

Defined in `shared/errors/exceptions.py`:

| Exception | HTTP Code | When Raised |
|-----------|-----------|-------------|
| `BadRequestError` | 400 | Validation failure, missing required field |
| `UnauthorizedError` | 401 | Missing/invalid/expired JWT |
| `AccountDeactivatedError` | 401 | User.isActive = false on login |
| `ForbiddenError` | 403 | Wrong role or not resource owner |
| `NotFoundError` | 404 | Entity not found by UUID |
| `ConflictError` | 409 | Already processed, duplicate, invalid status transition |

### 9.2 Error Response Shape

```json
{
  "code": "INVALID_STATUS_TRANSITION",
  "message": "Cannot transition from CON_HANG to DRAFT",
  "details": [
    { "field": "status", "message": "Invalid transition", "code": "invalid_transition" }
  ]
}
```

### 9.3 Error Code Inventory

| Code | HTTP | Description | Source |
|------|------|-------------|--------|
| `VALIDATION_ERROR` | 400 | Field-level validation failure | Generic |
| `ACCOUNT_DEACTIVATED` | 401 | User is inactive on login | USR-I02 |
| `UNAUTHORIZED` | 401 | Missing/invalid/expired token | Generic |
| `FORBIDDEN` | 403 | Insufficient role or not owner | Generic |
| `NOT_FOUND` | 404 | Entity not found | Generic |
| `ALREADY_PROCESSED` | 409 | Approval already decided | APP-I02 |
| `DUPLICATE_DEPOSIT` | 409 | Active deposit already exists | DE-I02 |
| `INVALID_STATUS_TRANSITION` | 409 | Status change violates state machine | LST-I01 |
| `MAX_HOT_ITEMS` | 409 | Exceeded 14 hot items | LST-C08 |
| `LAST_ADMIN` | 409 | Cannot deactivate/change last admin | USR-I01 |
| `USERNAME_TAKEN` | 409 | Username already in use | USR-C01 |

---

## 10. Security

### 10.1 JWT Authentication

```python
# Token creation (platform/security.py)
def create_access_token(user_id: UUID, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Token validation (platform/auth.py)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepo = Depends(UserRepo),
) -> UserEntity:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = await user_repo.get(UUID(payload["sub"]))
    if user is None or not user.is_active:
        raise UnauthorizedError()
    return user
```

### 10.2 Role-Based Access

```python
# Declarative role guard
require_admin = require_role(UserRole.ADMIN)
require_approver = require_role(UserRole.APPROVER, UserRole.ADMIN)
require_agent = require_role(UserRole.AGENT, UserRole.APPROVER, UserRole.ADMIN)

# Used in router:
@router.post("/", dependencies=[Depends(require_admin)])
```

### 10.3 Ownership Guard

Used in mutating facades for listings, pins, deal events. The `current_user` must either be the resource owner or have ADMIN role:

```python
def guard_owner(resource: HasOwner, current_user: UserEntity):
    if resource.created_by_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Not the resource owner")
```

### 10.4 Permission Matrix

| Action | AGENT | APPROVER | ADMIN |
|--------|-------|----------|-------|
| Browse listings | ✓ | ✓ | ✓ |
| Create listing | ✓ | ✗ | ✓ (auto-approve) |
| Edit own listing | ✓ | ✗ | ✓ |
| Delete DRAFT listing | ✓ (own) | ✗ | ✓ |
| Report deal event | ✓ | ✗ | ✓ |
| Report deal on own listing | ✓ | ✗ | ✓ |
| Report deal on any listing | ✓ | ✗ | ✓ |
| View approval queue | ✗ | ✓ | ✓ |
| Approve/reject | ✗ | ✓ | ✓ |
| Manage hot products | ✗ | ✗ | ✓ |
| Manage users | ✗ | ✗ | ✓ |
| View notifications | ✓ (own) | ✓ (own) | ✓ (all) |
| Pin/unpin | ✓ | ✓ | ✓ |

> **Decision**: Any agent can report deal events on any listing (BR-004 confirmed by product-overview.md). Owner-only preconditions in user flows were overridden.

---

## 11. Registration in `main.py`

```python
from src.modules import auth, users, listings, listing_images, deal_events
from src.modules import approvals, notifications, hot_products, pins, user_settings

MODULES = [
    auth.module,
    users.module,
    listings.module,
    listing_images.module,
    deal_events.module,
    approvals.module,
    notifications.module,
    hot_products.module,
    pins.module,
    user_settings.module,
]

def create_app() -> FastAPI:
    app = FastAPI(title="Biglands API", version="1.0.0")
    container = Container()
    container.configure()
    for module_fn in MODULES:
        router, prefix = module_fn()
        app.include_router(router, prefix="/api/v1")
    return app
```

---

## 12. Future Migrations

### 12.1 To Implement Later (Out of Scope v1)

| Entity | Module | Depends On | Priority |
|--------|--------|------------|----------|
| Review | `reviews` | Text-only reviews, auto-published, max 1 per user per listing | Done |
| ReviewImage | `reviews` | Review images table, max 10 per review | Done |
| Organization | `orgs` | Admin-managed orgs with user FK | Done |
| Notification preferences persistence | `user_settings` | Current scope — added as JSONB on User | In scope |

### 12.2 Resolved Contradictions (Implementation Decisions)

| Contradiction | Decision for v1 | Source |
|---------------|-----------------|--------|
| C-02: Deposit timing | Immediate DA_COC on approver confirm (no intermediate pending) | Simpler state machine |
| C-07: Commission required for CHO_THUE | Yes, required for all transaction types | BR-008, SC-004 |
| C-08: Image required vs recommended | Required for submission (server-enforced). DRAFT may have 0 images | BR-007 |
| C-11: Admin creates listings | Yes, with auto-approval (skip PENDING_APPROVAL) | SC-006 admin tab behavior |
| C-03: Deal action permissions | Any agent can report on any listing (BR-004) | product-overview.md, BR-004 |
| C-01: Commission for CHO_THUE | Required for all transaction types | Same as C-07 resolution |
| C-04: Notification preferences | In scope — US-003-notification-preferences kept as "Could Have" | US-003 exists |
| C-09: Immediate vs pending DA_COC | Immediate DA_COC on approver confirm (same as C-02) | Simpler state machine |

---

*End of Architecture — Biglands v1.0*
