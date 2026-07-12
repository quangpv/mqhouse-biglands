# Backend Architecture

## Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Framework | FastAPI | Async Python web framework |
| ORM | SQLAlchemy 2.0 (async) | Database access with asyncpg driver |
| Migrations | Alembic | Database schema versioning |
| Validation | Pydantic v2 + pydantic-settings | Request/response models, configuration |
| Auth | python-jose (JWT) + passlib (bcrypt) | Token generation, password hashing |
| Scheduler | APScheduler | Background cron jobs |
| Email | smtplib + Jinja2 templates | Async email sending |
| Image Processing | Pillow | Image optimization (WebP, thumbnails) |
| Search | unidecode | Vietnamese text transliteration |
| Server | uvicorn | ASGI server |

## Application Entry Point

`src/main.py` — `create_app()`:

1. Creates FastAPI instance with settings from config
2. Registers instance into custom DI container
3. Iterates through `MODULES` list (22 modules)
4. Each module resolved via `container.resolve()` (dependency injection)
5. If module returns `APIRouter`, included in app with prefix

```python
MODULES = [
    error_handler_module,    # Platform: global exception handlers
    scheduler_module,        # Platform: APScheduler lifecycle
    bootstrap_module,        # Platform: directory creation, static files
    auth_module,             # /auth
    users_module,            # /users
    organizations_module,    # /organizations
    properties_module,       # /properties
    approvals_module,        # /approvals
    files_module,            # /files
    geography_module,        # /geography
    transaction_types_module,# /transaction-types
    property_types_module,   # /property-types
    profile_module,          # /me
    notifications_module,    # /notifications
    reviews_module,          # /properties/{id}/reviews
    hots_module,             # /properties/hots
    pins_module,             # /properties/{id}/pins
    tags_module,             # /tags
    supports_module,         # /supports
    master_data_module,      # /master-data
    backfills_module,        # /backfills
    carts_module,            # /carts
    ws_module,               # /ws
]
```

## Dependency Injection Container

Custom lightweight container (`platform/container.py`):

- `Container` class with `_registry: dict[type, Callable[[], Any]]`
- `register(cls, factory)` — registers a class with optional factory
- `__setitem__` — registers a singleton instance
- `resolve(target)` — inspects `target`'s signature via `inspect.signature()`, auto-injects matching registered types

**Pattern:** Pure constructor-injection with automatic parameter resolution. Single global instance: `container = Container()`.

```python
# Registration
container[Settings] = settings          # singleton
container[UserRepo] = UserRepo          # factory (new instance per resolve)

# Resolution
repo = container.resolve(UserRepo)     # auto-injects AsyncSession via Depends
```

## Configuration

Pydantic Settings v2 (`platform/config.py`):

| Group | Keys | Defaults |
|---|---|---|
| App | `app_name`, `debug` | "Biglands", false |
| Database | `db_host`, `db_port`, `db_user`, `db_password`, `db_name` | localhost:5432 |
| JWT | `secret_key`, `jwt_algorithm`, `jwt_expire_minutes`, `jwt_refresh_expire_minutes` | HS256, 1440 (24h), 10080 (7d) |
| SMTP | `smtp_host`, `smtp_port`, `smtp_user`, `smtp_password`, `email_from` | — |
| Upload | `max_upload_size_mb`, `storage_backend` | 10, "local" |
| Business | `expiration_days`, `max_hot_items` | 30, 14 |
| Logging | `log_level`, `log_format` | INFO |

Loads from `.env` file. Computed properties: `database_url`, `upload_dir`, `log_dir`.

## Database

### Async SQLAlchemy Setup (`platform/database.py`)

- Engine: `create_async_engine` with `asyncpg` driver
- Pool: `pool_size=20`, `max_overflow=10`, `pool_recycle=3600`, `pool_pre_ping=True`
- Session: `expire_on_commit=False`
- `get_session()` — async generator with auto-commit/rollback/close
- `get_db()` — FastAPI `Depends()` wrapper

### Entity Base (`data/entities/_base.py`)

- `Base` — SQLAlchemy `DeclarativeBase`
- `TimestampMixin` — `created_at`, `updated_at` (server-side `func.now()`)
- `UUIDMixin` — `id: UUID` primary key (auto-generated `uuid4`)

### Entity Inventory (23 entities)

| Entity | Table | Key Relationships |
|---|---|---|
| `UserEntity` | `users` | → Organization, AvatarFile, UserTransactionType, UserPropertyType |
| `OrganizationEntity` | `organizations` | → OrgTransactionType, OrgPropertyType |
| `PropertyEntity` | `properties` | → TransactionType, PropertyType, Creator, Tags, Images, Certificates, Transitions, Reviews, Approvals, HotProperties |
| `ApprovalEntity` | `approvals` | → Property, Transition, DecisionTransition, TransactionType |
| `PropertyTransitionEntity` | `property_transitions` | → Property, Actor(User), Files |
| `FileEntity` | `files` | → Thumbnails |
| `FileThumbnailEntity` | `file_thumbnails` | → File |
| `ReviewEntity` | `reviews` | → Property, Author(User), Images(ReviewFile) |
| `ReviewFileEntity` | `review_files` | → Review, → File |
| `PropertyImageEntity` | `property_images` | → Property, → File |
| `PropertyCertificateEntity` | `property_certificates` | → Property, → File |
| `PropertyTagEntity` | `property_tags` | → Property, → Tag (join table) |
| `TransitionFileEntity` | `transition_files` | → Transition, → File |
| `HotPropertyEntity` | `hot_properties` | → Property, → User |
| `PinEntity` | `pins` | Composite PK (user_id, property_id) |
| `TagEntity` | `tags` | String PK (`id`) |
| `NotificationEntity` | `notifications` | → User |
| `TransactionTypeEntity` | `transaction_types` | String PK (`id`) |
| `PropertyTypeEntity` | `property_types` | String PK (`id`) |
| `RefreshTokenEntity` | `refresh_tokens` | → User |
| `TokenBlacklistEntity` | `token_blacklist` | Standalone (JTI-based) |
| `UserTransactionTypeEntity` | `user_transaction_types` | Join table |
| `UserPropertyTypeEntity` | `user_property_types` | Join table |

**Design decisions:**
- UUID primary keys (except lookup tables with string PKs)
- PostgreSQL-specific: `UUID`, `TSVECTOR`, `JSONB`
- Computed column: `search_vector` (persisted `to_tsvector`)
- Soft delete: `deleted_at` on `FileEntity` and `PropertyEntity`
- Relationship loading: mix of `lazy="selectin"`, `lazy="raise"` with explicit eager loading in repos

### Migrations

- Alembic with async support (`asyncpg`)
- 29 migration files covering: initial schema, enum additions, FK constraints, indexes, FTS support, file restructuring, notifications, tags, certificates

## Module Pattern

Every module follows consistent structure:

```
module_name/
  __init__.py          # module() → returns APIRouter or registers scheduler jobs
  router.py            # FastAPI APIRouter with route definitions
  schemas.py           # Pydantic request/response models
  mapper.py            # Entity ↔ Response/Request mapping
  facades/             # Business logic (one file per use case)
    use_case_name.py   # Async function with Depends-injected dependencies
```

### Route Handler Pattern

The facade function IS the handler:

```python
@router.post("", response_model=PropertyResponse)
async def create_property(result: PropertyResponse = Depends(create_property_facade)):
    return result
```

### Module Registration

```python
# Simple module
def module():
    return router

# Module with scheduler
def module():
    scheduler = container.resolve(AppScheduler)
    scheduler.add_job(cleanup_orphaned_files, trigger="interval", hours=24)
    return router
```

## Repository Pattern

Base class `Repo` (`data/repositories/_base.py`):
- Takes `AsyncSession` via `Depends(get_db)`
- Provides `paginated_list()` helper (count + offset/limit)
- Provides `calc_total_pages()` utility

### 17 Repositories

| Repository | Key Responsibilities |
|---|---|
| `UserRepo` | Search, get by username/email/roles/organization, eager loading |
| `PropertyRepo` | Most complex (~500 lines): search with 15+ filters, FTS ranking, transition CRUD, image/certificate sync |
| `ApprovalRepo` | Search with joins, count by transaction type/action |
| `NotificationRepo` | List by user, category counts, mark read |
| `FileRepo` | CRUD + path queries |
| `TagRepo` | CRUD with slug lookup |
| `HotPropertyRepo` | Time-window queries, ordering |
| `PinRepo` | Composite PK operations |
| `ReviewRepo` | Property-scoped queries |
| `ThumbnailRepo` | Thumbnail CRUD |
| `OrganizationRepo` | CRUD with user count check |
| `RefreshTokenRepo` | Token hash lookup, revoke |
| `TokenBlacklistRepo` | JTI blacklist check |
| `TransactionTypeRepo` | CRUD |
| `PropertyTypeRepo` | CRUD |
| `GeographyRepo` | Static JSON data |
| `BackfillRepo` | Search text computation |

## Platform Layer

### Authentication (`platform/auth.py`)

| Dependency | Purpose |
|---|---|
| `get_current_user()` | Full JWT extraction: header → decode → blacklist check → user load → active check |
| `require_auth()` | Thin wrapper requiring valid user |
| `require_role(*roles)` | Checks `current_user.role.value in roles` |

### Error Handling

Custom exceptions → centralized handlers → structured JSON:

| Exception | HTTP Status | Error Code |
|---|---|---|
| `NotFoundError` | 404 | `NOT_FOUND` |
| `ConflictError` | 409 | `CONFLICT` |
| `BadRequestError` | 400 | `VALIDATION_ERROR` |
| `UnauthorizedError` | 401 | `UNAUTHORIZED` |
| `ForbiddenError` | 403 | `FORBIDDEN` |

Also catches SQLAlchemy `IntegrityError` and parses PostgreSQL error messages.

### Scheduler (`platform/scheduler.py`)

- APScheduler `AsyncIOScheduler` wrapped in `AppScheduler`
- Registered as singleton in DI container
- Started/stopped via FastAPI lifespan
- Jobs registered by modules during initialization

### WebSocket Manager (`platform/ws_manager.py`)

- `ConnectionManager` — in-memory, maps `user_id → list[WebSocket]`
- Supports multiple simultaneous connections per user
- Dead connection auto-cleanup on send failure
- Singleton: `get_ws_manager()`

### Email Service (`platform/email.py`)

- Abstract: `EmailService` protocol
- Concrete: `SmtpEmailService` (sync via `asyncio.to_thread`)
- Templates: Jinja2 HTML (`welcome.html`, `password_reset.html`, `password_changed.html`)

### File Storage (`platform/storage.py`)

- Protocol: `FileStorage` with `save()`, `get()`, `delete()`, `exists()`, `move()`, `get_url()`, `list_keys()`
- Implementation: `LocalFileStorage` — filesystem-based, base dir from `settings.upload_dir`

### Logger (`platform/logger.py`)

- `AppLogger` wrapping Python `logging`
- Dual output: stdout + rotating file (`app.log`, 10MB, 5 backups)

## Property State Machine

### States (13)

| Status | Terminal? |
|---|---|
| `draft` | No |
| `post_pending` | No |
| `edit_pending` | No |
| `deposit_pending` | No |
| `soldout_pending` | No |
| `complete_pending` | No |
| `cancel_pending` | No |
| `reopen_pending` | No |
| `available` | No |
| `deposited` | **Yes** |
| `soldout` | **Yes** |
| `expired` | **Yes** |
| `completed` | **Yes** |

### Transitions (7 actions)

| Action | SALE Target | ADMIN/APPROVER Target |
|---|---|---|
| Submit | POST_PENDING | AVAILABLE |
| Deposit | DEPOSIT_PENDING | DEPOSITED |
| Soldout | SOLDOUT_PENDING | SOLDOUT |
| Cancel | CANCEL_PENDING | AVAILABLE |
| Complete | COMPLETE_PENDING | COMPLETED |
| Reopen | REOPEN_PENDING | AVAILABLE |
| Edit (available) | EDIT_PENDING | Changes applied immediately |

### Withdraw Revert Mapping

| From Status | Returns To |
|---|---|
| POST_PENDING | DRAFT |
| DEPOSIT_PENDING | AVAILABLE |
| SOLDOUT_PENDING | AVAILABLE |
| CANCEL_PENDING | DEPOSITED |
| COMPLETE_PENDING | DEPOSITED |
| REOPEN_PENDING | from_property_status (stored in approval) |

### Transition Service

`TransitionService.invoke()` is the shared engine for deposit, soldout, cancel, complete:
- SALE: sets PENDING status, creates approval, sends notification
- ADMIN/APPROVER: sets final status directly, rejects any existing pending approval

## File Upload System

1. **Validation**: image/* only (no SVG), max 10MB, max 10 files
2. **Optimization**: JPEG/PNG/WebP → WebP (quality 85), resize if >1920px (Lanczos), RGBA/CMYK → RGB
3. **Storage**: `{user_id}/{file_uuid}.webp` via `FileStorage` protocol
4. **Thumbnails**: async generation of `320w` and `640w` variants (non-GIF only)
5. **Content hash**: SHA-256 computed and stored
6. **Trash**: deleted files moved to `trash/` dir, cleaned up after 30 days
7. **Orphan cleanup**: runs every 24 hours via scheduler

## Notification System

### 23 Event Types

Covering: listing creation/approval/rejection, deposit/soldout/cancel/complete reporting/confirmation/rejection, edit approval/rejection, expiration, reopen request/approval/rejection, listing update.

### Delivery

1. `NotificationService.notify_admins_and_approvers()` — creates notifications for all admins + org approvers
2. `NotificationService.notify_property_user()` — creates notification for property owner
3. After DB persist, sends real-time WebSocket push via `ConnectionManager`

### Title Formatting

Vietnamese action strings mapped from `NotificationType` enum via `notification_formatter.py`.

## Search System

### Vietnamese Normalization (`shared/search/normalize.py`)

1. Unicode NFKD normalization
2. Vietnamese diacritics removal (`đ` → `d`)
3. Abbreviation expansion: `cc` → `chung cu`, `hcm` → `ho chi minh`, `mt` → `mat tien`, etc.
4. Price shorthand: `1.5 ty` → `1.5 ty`, `500tr` → `500 trieu`

### Search Text Computation (`shared/search/search_text.py`)

Denormalized field built from: title, description, address, street, house number, ward/district/province names, label, furnishing, legal status, tags, property type, transaction type, formatted price.

### Full-Text Search

- PostgreSQL `TSVECTOR` computed column (`search_vector`)
- Ranking: `ts_rank` + trigram similarity + hot bonus + view count

## Scheduled Jobs

| Job | Schedule | Purpose |
|---|---|---|
| `expire_deposited_properties` | Daily cron | Expires deposited/deposit_pending properties past contract date |
| `cleanup_orphaned_files` | 24h interval | Removes temp files (>24h), trash (>30d), orphaned user files (>24h) |

## Testing

- **Framework**: pytest + pytest-asyncio (auto mode)
- **Database**: Dedicated test PostgreSQL on port 5445, auto-managed Docker container
- **Parallel**: pytest-xdist with per-worker databases (`biglands_test_{worker}`)
- **Pattern**: Schema drop/recreate per session, transaction-rollback per test
- **Fixtures**: `db_session`, `override_get_db`, `client` (httpx.AsyncClient), `FakeEmailService`, pre-seeded users
- **Coverage**: 22 test directories covering all modules

## Deployment

### Docker Compose

```yaml
services:
  app:   # GHCR image, port 8000, depends on db health
  db:    # PostgreSQL 16 Alpine, port 5444
```

Volumes: uploads, logs, database data.

### Startup Sequence (`scripts/start.sh`)

1. `alembic upgrade head` — apply migrations
2. `python -m scripts.migrate_files` — file migration
3. `python scripts/seed.py` — seed initial data (admin, org, types)
4. `uvicorn src.main:app --host 0.0.0.0 --port 8000`

### Dev Mode (`scripts/dev.sh`)

1. Creates/manages local Docker Postgres container
2. Runs migrations + seed
3. `uvicorn src.main:app --reload`
