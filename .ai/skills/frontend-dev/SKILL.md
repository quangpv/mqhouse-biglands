---
name: simple-frontend-dev
description:
  Apply this skill when the user asks to scaffold, structure, or review a React/TypeScript frontend project using a feature-based modular architecture. Triggers include: setting up folder structure, creating repositories, mappers, facade hooks, or DTO/UI types; questions about separating concerns in a frontend app; requests to "follow the architecture", "add a feature the right way", or "create a repository/hook/mapper". Also use when the user wants to enforce the View → Facade → Data layering pattern or when reviewing code for anti-patterns like API calls in components or mixed DTO/UI types.
techstack:
  languages:
    - JavaScript ES2023
    - TypeScript
  frameworks:
    - React
  styling:
    - TailwindCSS
  state-management:
    - Zustand
    - TanStack Query
  testing:
    - Vitest
    - Playwright
  build-tools:
    - Vite
  icons:
    - Lucide (icon components)
---

# Frontend Development Skill

## Overview

Three-layer architecture enforcing View → Facade → Data dependency flow. Every feature follows the same structure, naming, and data flow — DTO → mapping → UI. Eliminates fat components, mixed models, and layer skipping.

## Architecture

### Folder Structure

```
src/
├─ platform/                           # HTTP client, Query client, persistence
├─ data/                               # Data Layer
│  ├─ queries/                         # <feature>Queries.ts — query key factories + reusable use<Feature>Query hooks (useQuery only). Must NOT contain useMutation — mutations belong in facade action hooks.
│  ├─ repositories/                    # <feature>Repository.ts — API calls, return DTOs
│  ├─ types/                           # <Name>DTO type files
│  └─ utils/                           # serialization, deserialization at API boundary
├─ pages/<feature>/
│  ├─ facades/                         # use<Feature>State, use<Action><Feature>, use<Feature>Mapper
│  ├─ components/                      # View — UI components
│  ├─ constants/                       # View — UI presentation maps
│  ├─ types.ts                         # I<Name> UI types + zod schemas
│  └─ <PageName>.tsx                   # View — page component
├─ shared/
│  ├─ components/                      # View — reusable UI
│  ├─ context/                         # Cross-cutting (theme, locale, modal)
│  ├─ hooks/                           # Cross-cutting UI hooks
│  └─ utils/                           # Presentation formatting
├─ App.tsx / AppRoutes.tsx / main.tsx  # View — App Shell
└─ index.css                           # View — global styles
```

### Layer Dependency

| Layer | Depends on | Must Not Depend On |
|-------|-----------|--------------------|
| View | Facades only | Data layer, DTOs, `fetch` |
| Facade | Data layer, shared context/utils | View components, other feature facades |
| Data | Platform | UI types, View, Facade |
| Platform | — | UI types, View, Facade, Data |

### Error Flow

```
Platform (throws ApiError) → Data → Facade action hook (catches, fires toast) → View (reads error state, shows retry UI)
```

### Facade Coordination

State hooks own UI state, derived state, and UI interactions. Action hooks own business operations that mutate server state. They never import each other — action calls `queryClient.invalidateQueries()` on success, state reads via `useQuery`.

## Coding Standards

### File Organization

- Max ~200 lines per file; split at ~100 lines JSX for components
- One action hook per mutation (`useCreateUser`, `useUpdateUser`)
- One constants file per domain concept (`userUI.ts`, `roleUI.ts`)

### Control Flow

- DO use early returns / guard clauses over nested `if` blocks — flatten indentation, reduce cyclomatic complexity
- DO validate inputs at the top of a function and return early for edge cases

### State Management

Default: hooks + context. Introduce external state only when:

| When | Solution |
|------|----------|
| 3+ unrelated features share state | Zustand (light) or Redux (team-scale) |
| Complex undo/redo | Zustand + `temporal` |
| Multi-step wizard with cross-step validation | Zustand or dedicated context |
| Real-time collaborative | Zustand or Redux + middleware |
| Simple cross-feature (theme, auth) | React Context |

### Layer Rules

#### View Layer
- DO consume `use<Feature>State`, `use<Action><Feature>` only — these two hook types are the complete facade API for View; NEVER consume APIs, repositories, DTOs, or `fetch`
- DO work with `I<Name>` types only
- DO extract event handlers to named functions — no inline logic in JSX
- DO use Lucide icon components for all icons. Replace SVG icons with the matching Lucide component whenever available; otherwise, extract the SVG into a dedicated component at `shared/components/icons/<Name>Icon.tsx`.
- DO call `mutate(data)` unconditionally — guards and branching belong in facade; pass raw event arguments only — never compute mutation payloads, arrays, or derived data in View; View may read mutation result for local UI state resets only (eg. mode, dirty flags, selection) — server side effects (eg. navigate, toast) stay in action hook
- DO read error/loading state from facade; show retry UI
- NEVER use `useState`, `useReducer`, `useForm` or mutable refs in page components
- Context providers in `shared/context/` are View layer
  - **Component Context providers**: eg. Toast, Notification, Modal,...
  - **Domain Context providers**: (eg. Auth,...) follow all View rules above (facade hooks only, no API/DTO/fetch); export shared context `use<Name>Context`; do NOT place business logic, side effects, or data fetching in context; NEVER put mutation logic in shared context.
- Domain Modal/Dialog are View layer, it should follow all View rules
- All shared/reusable components must reside in `shared/components`

#### Facade Layer

##### `pages/<feature>/facades/` (View-facing API + internal utilities)
- Closed set: `use<Feature>State`, `use<Action><Feature>`, `use<Feature>Mapper`
- **State hooks** — own UI state (`useState` for eg. mode, flags, text, filters), derived state (eg. computed lists from queries), and non-mutation UI interactions (eg. navigate, showToast, open platform APIs, open modals, set filters, toggle views). Read server state via `useQuery` with query keys. Map DTOs to `I<Name>` internally via mapper — never expose DTOs to View. NEVER import action hooks.
- **Action hooks** — own business operations that mutate server state: validate via zod → mapper.toPayload() → repository.mutate() → queryClient.invalidateQueries() → side effects. Use `useMutation` with `onSuccess`/`onError`. Mutation-triggered side effects (eg. `navigate`, `showToast`) belong EXCLUSIVELY in action hooks — View must NOT call them after `mutate`. Never rethrow errors to View. NEVER Multiple mutations combined in a single facade hook (e.g., `useAuthActions` with login + register + logout)
    - Error handling: return errors View needs to display (eg. validation errors) from the action hook; handle flow error internally (eg. fire toast/notification for API/mutation errors). NEVER accept error callbacks.
- **Mapper hooks** — sole owner of DTO↔UI transformation both directions; carry raw DTO + derived display fields; depend only on DTO/UI types, shared context, shared utils; NEVER import from View components
  - `I<Name>` fields are **always camelCase**; DTO fields match the API. When the backend uses a different case (e.g., Python's snake_case), the mapper converts both directions — DTO→UI on reads, UI→DTO on mutation payloads.
- NEVER skip layers (no direct `httpClient` calls in facades)
- NEVER create combined facade hooks that import both state and action hooks

##### `pages/<feature>/types.ts` (zod schemas + UI types)
- For form data, define zod schemas as the **single source of truth** for validation and shape
- Derive `I<Name>` form types from the schema using `z.infer<typeof schema>`
- Keep additional UI-only fields (e.g., `rememberMe`, `confirmPassword`) in the schema alongside validation rules
- Facades import zod schemas for form validation — no hook wrapper needed since zod is pure functions
- NEVER import from `facades/`, View components, or Data layer

#### Data Layer
- Repositories call API via platform only, return DTOs — no UI types
- DTOs: one file per entity in `data/types/<entity>.dto.ts`, type-only; field names mirror the API (snake_case for Python/Django, camelCase for Node.js) — never required to be camelCase
- Platform: feature-agnostic, normalize errors to `ApiError`, retry with exponential backoff
- Query key factories: start simple (`{ all, me }`), graduate to hierarchical (`{ all, lists(), details() }`) when needed

### Naming

Variables should be named in English consistently.

| Pattern | Convention | Example          |
|---------|-----------|------------------|
| Display Types | `I<Name>` (type alias, `I` prefix convention) | `ITransactionType` |
| DTO Types | `<Name>DTO` (in `<name>.dto.ts`) | `UserDTO` |
| Form Types | Schema + `z.infer<typeof schema>` in `types.ts` | `loginSchema`, `ILoginForm = z.infer<typeof loginSchema>` |
| State Hook | `use<Feature>State` | `useUserState` |
| Action Hook | `use<Action><Feature>` | `useCreateUser` |
| Mapper Hook | `use<Feature>Mapper` | `useUserMapper` |
| Page | `<Name>Page` | `UsersPage`      |
| Repository | `<name>Repository` | `userRepository` |
| Query Keys | `<name>Queries` | `userQueries`    |
| UI Model Fields | `camelCase` — always, regardless of backend | `firstName`, `createdAt` |
| DTO Fields | Match API convention | `first_name` (Python), `firstName` (Node.js) |

### Imports

- `@/` maps to `src/` (alias) — use for all cross-directory imports
- Relative imports only for `./` (same dir) or `../` (parent)
- Omit file extensions

## Workflow

1. Read all rules below before writing code
2. Scaffold feature folder under `pages/<feature>/` with `types.ts` + `facades/` + `components/` + `constants/`
3. Define DTO → Repository → Query keys in `data/`
4. Define zod schemas in `types.ts` → implement mapper + facades (state/action hooks) → page component
5. Verify: no layer violations, no DTOs in View, all state named per conventions

## Quick Reference

- **ALWAYS** go View → Facade → Repository → Platform — never skip layers
- **ALWAYS** isolate features under `pages/<feature>/` — no cross-feature imports between facades
- **ALWAYS** call `mutate(data)` unconditionally from View — guards in facade only
- **ALWAYS** use Lucide icon components (`import { IconName } from "lucide-react"`)
- **ALWAYS** use `@/` alias for cross-directory imports
- **NEVER** use `useState`/`useReducer` in page components
- **NEVER** import DTO types in View
- **NEVER** call `httpClient` outside `platform/`
- **NEVER** construct DTO types in facade hooks — delegate to mapper
- **ALWAYS** derive `I<Name>` from zod schema via `z.infer<typeof schema>` — never manually redefining fields
- **ALWAYS** use camelCase for `I<Name>` fields; DTO naming follows the API; mapper bridges any case mismatch
