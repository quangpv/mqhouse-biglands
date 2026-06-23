---
name: backend-patterns
description: |
  Async-FastAPI + SQLAlchemy backend pattern with facade-per-use-case architecture.
  3-layer structure (Router → Facade → Data) with custom DI container, JWT auth,
  and PostgreSQL. Module-organized with one Pydantic-schema file, one mapper file,
  and per-use-case facade files under each module.
techstack:
  languages:
    - Python 3.10+
  frameworks:
    - FastAPI
    - SQLAlchemy 2.x (async)
    - Alembic
    - Pydantic v2
  testing:
    - pytest
    - pytest-asyncio
    - httpx (TestClient)
  build-tools:
    - uvicorn
    - docker-compose
  database:
    - PostgreSQL 16
    - asyncpg
  background-tasks:
    - asyncio.Queue (custom BackgroundExecutor)
---

# Backend Development Skill

## Overview

A lightweight async-FastAPI + SQLAlchemy architecture for building CRUD backends. The signature pattern is **one facade file per use case** — thin routers delegate to facades which orchestrate repositories and services.

Use this skill when building:
- RESTful JSON APIs with Python
- Async PostgreSQL backends
- Auth-enabled (JWT) services
- Feature-organized modules with clear separation of concerns

**Trigger phrases:** "create a backend", "build an API", "new FastAPI project", "add a module", "implement a use case"

---

## Architecture

### Folder Structure

```
src/
├── __init__.py
├── main.py                          # App entry point: load_modules() → FastAPI
├── platform/
│   ├── __init__.py
│   ├── config.py                    # Pydantic BaseSettings (env vars)
│   ├── container.py                 # Custom DI container (inspect-based)
│   ├── database.py                  # async_session_factory, get_session generator
│   ├── auth.py                      # get_current_user, require_auth dependencies
│   ├── security.py                  # hash_password, verify_password, JWT create/decode
│   ├── dependencies.py              # Shared FastAPI dependencies (get_db, executor)
│   ├── logger.py                    # Abstract AppLogger, ConsoleLogger/FileLogger, access log middleware
│   ├── background.py                # BackgroundExecutor (asyncio queue), RunExecutor
│   ├── scheduler.py                 # AppScheduler wrapping APScheduler + lifespan
│   └── email.py                     # Pluggable EmailService (stub)
├── data/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py              # Re-exports all entities
│   │   ├── _base.py                 # SQLAlchemy DeclarativeBase
│   │   └── <entity>.py             # One file per table (Mapped columns, relationships)
│   └── repositories/
│       ├── __init__.py              # Re-exports all repos
│       └── <entity>_repo.py         # One repo per entity (create, get, list, update, delete)
├── modules/
│   ├── __init__.py
│   └── <module>/
│       ├── __init__.py
│       ├── router.py                # FastAPI APIRouter, route definitions only
│       ├── schemas.py               # Pydantic request/response models
│       ├── mapper.py                # Entity ↔ Schema conversion functions
│       └── facades/
│           ├── __init__.py
│           └── <use_case>.py        # One async function per use case (business logic)
└── shared/
    ├── __init__.py
    ├── errors/
    │   ├── __init__.py
    │   └── exceptions.py            # Custom HTTPException subclasses
    ├── pagination/
    │   └── __init__.py              # Reusable pagination schemas
    └── utils/
        └── __init__.py              # Shared utility functions
```

### Layer Dependency

```
Router (HTTP) → Facade (business logic) → Repository (data access)
                    ↕                              ↕
               Platform services               Entities (ORM)
           (auth, logger, email, scheduler)
```

- **Routers must NOT contain business logic** — only route decorators, `Depends()` calls, and `response_model` declarations.
- **Facades must NOT reference HTTP concerns** (Request, Response, status codes) — they return domain/Pydantic objects and raise typed exceptions.
- **Repositories must NOT contain business logic** — only raw CRUD queries.

### Error Flow

```
Facade raises HTTPException (or custom subclass)
       ↓
FastAPI catches → returns JSON error response
```

Standard error types to create in `shared/errors/exceptions.py`:
- `NotFoundError` → 404
- `ConflictError` → 409
- `BadRequestError` → 400

### Facade Coordination

```
┌─────────────────────────────────────────────────┐
│                  Facade Function                 │
│  async def <use_case>(                           │
│      data: <RequestSchema> = Depends(),          │
│      repo: <Repo> = Depends(<Repo>),             │
│      user: UserEntity = Depends(get_current_user),│
│  ) -> <ResponseSchema>:                           │
│      # 1. Validate / check preconditions          │
│      # 2. Call repo methods                       │
│      # 3. Log significant events                  │
│      # 4. Return response schema                  │
└─────────────────────────────────────────────────┘
```

- One facade file per use case (e.g., `create_note.py`, `update_note.py`)
- All dependencies injected via FastAPI `Depends()`
- No shared mutable state between facades

---

## Coding Standards

### File Organization

Each file follows this section order:
1. Standard library imports
2. Third-party imports (blank line separator)
3. Local imports (blank line separator)
4. Constants (UPPER_CASE)
5. Functions/Classes

### Control Flow

```python
# DO: Early return / early raise
user = await repo.get_by_email(email)
if user is None:
    raise NotFoundError("User not found")

# DON'T: Nested if-else pyramids
```

### State Management

- Entities are mutable ORM objects — mutations happen inside facades via mapper functions
- No global mutable state — everything is injected via DI container
- Config is a singleton `settings` instance loaded once at startup

### Layer Rules

#### Router Layer

| # | Rule | Rationale |
|---|------|-----------|
| 1 | Route definitions only — no business logic, no data access | Keeps HTTP layer anemic, testable, replaceable |
| 2 | Each endpoint calls exactly one `Depends(facade_fn)` and returns its result | Router is a pure delegator |
| 3 | All dependencies wired via `Depends()` — never `Repo(db=session)` inline | Enables DI override in tests |
| 4 | Declare `response_model` and `status_code` on every route decorator | Self-documenting API contract |
| 5 | Protect routes via `dependencies=[Depends(require_auth)]` for read endpoints, `dependencies=[Depends(require_role("role"))]` for admin endpoints | Declarative, inspectable auth — facades should not carry pure auth guards |
| 6 | Path params captured as function arguments, forwarded to facade | FastAPI handles parsing/validation |
| 7 | Router exposed via a top-level `module()` function returning `APIRouter` | Consistent registration in `main.py` |

```python
# DO:
@router.get("/{note_id}", response_model=NoteResponse, dependencies=[Depends(require_auth("user"))])
async def get(result: NoteResponse = Depends(get_note_facade)):
    return result

# DON'T — business logic in router:
@router.get("/{note_id}")
async def get(note_id: UUID, repo: NoteRepo = Depends(NoteRepo)):
    note = await repo.get(note_id)  # belongs in facade
    return note_to_response(note)   # belongs in facade
```

#### Facade Layer

| # | Rule | Rationale |
|---|------|-----------|
| 1 | One file, one async function — `facades/create_note.py` exports `create_note` | Navigable, testable, merge-friendly |
| 2 | All dependencies via `Depends()` — repos, services, current_user | Testable via dependency overrides |
| 3 | Return a Pydantic response schema — never a raw entity | Decouples internal model from API shape |
| 4 | Raise typed exceptions (`NotFoundError`, `ConflictError`) for rule violations | FastAPI maps them to HTTP codes automatically |
| 5 | Use mapper functions for entity↔schema conversion — never build entities inline | Single place to update mappings |
| 6 | Do NOT reference HTTP primitives (`Request`, `Response`, `status`, `JSONResponse`) | Facade stays domain-pure |
| 7 | Single responsibility — one precondition check + one repo call per facade | Testable, predictable |

```python
async def create_note(
    data: NoteCreateRequest = Depends(),
    repo: NoteRepo = Depends(NoteRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> NoteResponse:
    note = build_note(data, created_by=current_user.id)
    note = await repo.create(note)
    logger.info("Created note %s (user=%s)", note.id, current_user.id)
    return note_to_response(note)
```

#### Data Layer

**Entities:**

| # | Rule | Rationale |
|---|------|-----------|
| 1 | One file per entity — filename: `<entity>.py` | Navigable, grep-friendly |
| 2 | Extend `Base` (DeclarativeBase from `_base.py`) | Single metadata source for Alembic |
| 3 | Use `Mapped[...]` annotations + `mapped_column()` | SQLAlchemy 2.x modern style |
| 4 | `__tablename__` is plural snake_case (`"notes"`, `"users"`) | Conventional, matches DB naming |
| 5 | Timestamps use `server_default=func.now()` — never `default=datetime.now` | DB-controlled, consistent across runs |
| 6 | PKs are `UUID(as_uuid=True)` with `default=uuid.uuid4` | Distributed-safe, no sequential leaks |
| 7 | All datetime columns use `DateTime(timezone=True)` | Timezone-aware, avoids DST bugs |

```python
class NoteEntity(Base):
    __tablename__ = "notes"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
```

**Repositories:**

| # | Rule | Rationale |
|---|------|-----------|
| 1 | One repo class per entity — named `<Entity>Repo` | Matches entity granularity |
| 2 | Constructor takes `db: AsyncSession = Depends(get_db)` — never create sessions | Session managed by platform/database.py |
| 3 | Methods operate on entities only — never return Pydantic schemas | Repo speaks ORM; facade handles mapping |
| 4 | Raw SQLAlchemy queries only — no business logic or validation | Repo is a data gateway, not a service |
| 5 | Singular queries return `Entity | None` — never raise HTTP exceptions | Let facade decide the HTTP response |
| 6 | Each mutating method commits its own transaction | Simple, predictable transaction boundaries |
| 7 | Soft-delete: `delete()` sets `deleted_at`; `hard_delete()` removes row | Two explicit methods for two semantics |

```python
class NoteRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, note_id: UUID) -> NoteEntity | None:
        result = await self.db.execute(
            select(NoteEntity).where(NoteEntity.id == note_id)
        )
        return result.scalar_one_or_none()
```

**Mapper:**

| # | Rule |
|---|------|
| 1 | Mapper module exposes three standard functions: `request_to_entity`, `apply_to_entity`, `entity_to_response` |
| 2 | Default path: facades delegate entity construction to `request_to_entity(body)` and field updates to `apply_to_entity(entity, body)` |
| 3 | The mapper is the canonical place for ORM constructor calls and field set expressions — facades orchestrate, mappers transform |
| 4 | `entity_to_response` reads relationship collections from the entity object instead of accepting UUID list parameters |

### Naming

| Category | Convention | Example |
|---|---|---|
| Files/dirs | `snake_case` | `create_note.py`, `note_repo.py` |
| Module dirs | `snake_case` | `auth/`, `notes/` |
| Façade dir | `facades/` | fixed name |
| Classes (entities) | `PascalCase + Entity` | `UserEntity`, `NoteEntity` |
| Classes (schemas) | `PascalCase + Request/Response` | `NoteCreateRequest`, `NoteResponse` |
| Classes (repos) | `PascalCase + Repo` | `NoteRepo`, `UserRepo` |
| Functions (facades) | `snake_case` (verb) | `create_note`, `list_notes` |
| Functions (mappers) | `snake_case` (verb + noun) | `request_to_entity`, `apply_to_entity`, `entity_to_response` |
| Variables | `snake_case` | `hashed_password`, `access_token` |
| Base file | `_base.py` | fixed name |

### Imports

```python
# Standard library
import uuid
from datetime import datetime, timezone

# Third-party
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from src.data.entities import NoteEntity
from src.data.repositories import NoteRepo
from src.platform.dependencies import get_db
```

- One import per line
- Grouped: stdlib → third-party → local, with blank line separators
- Use absolute imports from `src.` always

### Testing
- Write tests from a business perspective, not a technical perspective. Test names must be written in business language that a product owner or customer can understand. Each test should describe a business outcome, not a technical action.

- Each facade function should have its own dedicated test file. 

---

## Workflow

### Adding a New Module

1. Create `src/modules/<name>/`
2. Create `schemas.py` — Pydantic request/response models
3. Create `mapper.py` — Entity↔Schema converters
4. Create `facades/<use_case>.py` — one file per endpoint
5. Create `router.py` — route definitions using `Depends(facade_fn)`
6. Register in `main.py` by adding module function to `MODULES` list
7. Create `tests/test_<module>/` — one file per use case
8. Run Alembic migration if entity changes

### Adding a New Entity

1. Create `src/data/entities/<entity>.py` — ORM model
2. Export in `src/data/entities/__init__.py`
3. Create `src/data/repositories/<entity>_repo.py` — CRUD methods
4. Export in `src/data/repositories/__init__.py`
5. Run migration: `alembic revision --autogenerate -m "add <entity> table"`

### Running

```bash
./run.sh dev       # Postgres + migrations + uvicorn
./run.sh test      # Postgres + pytest
./run.sh db        # Postgres + migrations only (no app)
./run.sh migrate   # Autogenerate + apply migration
```

---

## Quick Reference

### Key Files

| File | Purpose |
|---|---|
| `main.py` | App assembly: modules → DI container → FastAPI |
| `src/platform/container.py` | `Container` — type-based DI resolution |
| `src/platform/config.py` | `Settings(BaseSettings)` — env config |
| `src/platform/database.py` | `async_session_factory`, `get_session` |
| `src/platform/security.py` | JWT create/decode, bcrypt hash/verify |
| `src/platform/dependencies.py` | Shared `Depends()` callables |
| `src/shared/errors/exceptions.py` | Custom HTTP exceptions |

### Boilerplate Templates

**Router:**
```python
from fastapi import APIRouter, Depends, status
from src.modules.<module>.facades.<use_case> import <use_case>

def module():
    router = APIRouter(prefix="/<route>", tags=["<tag>"])
    @router.post("/", response_model=<Res>, status_code=status.HTTP_201_CREATED)
    async def create_endpoint(result: <Res> = Depends(<use_case>)):
        return result
    return router
```

**Facade:**
```python
from fastapi import Depends
from src.data.repositories import <Entity>Repo
from src.modules.<module>.schemas import <Req>, <Res>

async def <use_case>(
    data: <Req> = Depends(),
    repo: <Entity>Repo = Depends(<Entity>Repo),
) -> <Res>:
    # business logic
    return <Res>(...)
```

**Repository:**
```python
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.entities import <Entity>
from src.platform.dependencies import get_db

class <Entity>Repo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    # CRUD methods
```

---

## Customization Points

### Must customize per project:
| Item | Location |
|---|---|
| Project name / API title | `main.py` — `FastAPI(title=...)` |
| Entity definitions | `src/data/entities/*.py` |
| Module/routes | `src/modules/<module>/` |
| Business logic | Facade files |
| Docker credentials/ports | `docker-compose.yml`, `config.py` |
| Test DB config | `conftest.py`, `config.py` |

### Must NOT change (core conventions):
- 3-layer + Platform structure
- Facade-per-use-case pattern (one file, one function)
- Router → `Depends(Facade)` delegation
- Repository pattern with `Depends(get_db)`
- Pydantic schemas for I/O validation
- Alembic for schema migrations
- Integration test pattern (Docker Postgres, per-table cleanup)
- `Container` class for DI
- Async-first (`async/await` everywhere)
