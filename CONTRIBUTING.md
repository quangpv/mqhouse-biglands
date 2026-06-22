# Contributing

## Tech Stack

- **Frontend**: Vite + React + TypeScript, shadcn/ui, TanStack Query, Zustand, React Hook Form + Zod
- **Backend**: Python + FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Auth**: JWT (access token)

## Project Structure

```
biglands/
├── backend/
│   └── src/
│       ├── main.py              # App entry point
│       ├── platform/            # Config, DI container, auth, DB, bootstrap
│       ├── shared/              # Errors, pagination, utilities
│       ├── data/                # Entities, repositories
│       └── modules/             # Feature modules (auth, users, listings, etc.)
│           └── {module}/
│               ├── router.py         # FastAPI router (thin)
│               ├── facades/          # Business logic + DI
│               └── schemas.py        # Pydantic request/response schemas
├── frontend/
│   └── src/
│       ├── App.tsx              # Routes
│       ├── pages/               # Feature pages
│       │   └── {feature}/
│       │       ├── {name}-page.tsx       # View (calls state + action hooks)
│       │       ├── facades/              # State hooks + action hooks
│       │       ├── components/           # UI components
│       │       └── types.ts              # Form interfaces
│       ├── data/
│       │   ├── types/           # DTOs (camelCase, match OpenAPI spec)
│       │   ├── repositories/    # API calls via HTTP client
│       │   ├── queries/         # TanStack Query key factories
│       │   └── infra/           # HTTP client, QueryClient
│       └── shared/
│           ├── components/      # Shared UI (AppLayout, AuthGuard, shadcn/ui)
│           ├── hooks/           # Shared hooks
│           └── context/         # Auth context + store
├── docs/
│   └── openapi.yaml             # API spec (source of truth)
└── .ai/                         # AI-assisted development plans
```

## Frontend Architecture

### Layering (per feature page)

1. **View** (`{name}-page.tsx`): calls state hook + action hook, reads data, renders components. Never calls mutate/useState/navigate/toast directly.
2. **State Hook** (`use{Feature}State.ts`): owns RHF form via `useForm` + Zod resolver, manages UI state. Returns `form`, `schema`, and state values.
3. **Action Hook** (`use{Feature}.ts`): owns mutations via `useMutation`, side effects (navigation, toast, query invalidation).
4. **Component** (`{name}.tsx`): receives `form`, `onSubmit`, `isPending`, `error` as props. Pure presentational.

### Conventions

- Vietnamese labels and toast messages
- DTOs in `data/types/` match `docs/openapi.yaml` (camelCase)
- Repositories in `data/repositories/` — one per API domain
- Query key factories in `data/queries/` for cache invalidation
- shadcn/ui components under `shared/components/ui/`

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
cp .env.example .env    # configure PostgreSQL connection
alembic upgrade head
uvicorn src.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev             # runs on port 5173, proxies /api to backend
```

## Commit Messages

Follow conventional commits:

```
feat: add approval queue filter
fix: handle empty listing images
refactor: extract pagination logic
```

## Pull Request Process

1. Ensure the feature works with the actual backend API
2. Verify no TypeScript errors (`npm run typecheck` or `tsc --noEmit`)
3. Keep PRs focused on a single feature/module
