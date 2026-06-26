# Frontend Architecture

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | React 19 + TypeScript | Component framework |
| Build | Vite 8 | Dev server + bundler |
| Routing | react-router-dom v7 | SPA navigation |
| Server State | TanStack React Query v5 | Caching, fetching, mutations |
| Client State | Zustand v5 | Auth state, UI preferences |
| HTTP | Axios 1.18 | API client |
| Forms | React Hook Form v7 + Zod v4 | Form state + validation |
| Styling | Tailwind CSS v4 + shadcn/ui | Utility-first CSS + primitives |
| Icons | Lucide React | Icon library |

## Architecture Pattern

**View → Facade → Data → Platform** — three-layer strict dependency flow.

Each feature is self-contained under `pages/<feature>/` with its own facades, components, constants, and Zod schemas. Features never import from each other's facades.

### Layer Dependency Rules

| Layer | Files | Depends On | Must NOT import |
|---|---|---|---|
| **View** | `pages/*/LoginPage.tsx`, shared components, layouts | Facades only | Data layer, DTOs, `httpClient`, repositories, query keys |
| **Facade** | `pages/*/facades/*.ts`, `pages/*/types.ts` | Data layer, shared context/utils | View components, other feature facades |
| **Data** | `data/repositories/*.ts`, `data/queries/*.ts`, `data/types/*.dto.ts` | Platform | UI types, View, Facade |
| **Platform** | `platform/*.ts` | — | UI types, View, Facade, Data |

### Error Flow

```
Platform (throws ApiError)
  → Data layer (passes through)
  → Facade action hook (catches, maps to UI errors, fires toast/navigate)
  → View (reads error state, shows retry UI, field-level errors)
```

## Project Structure

Only the login feature is defined here. Other features follow the same pattern when added.

```
src/
├─ platform/
│   ├─ httpClient.ts                # Axios instance with auth interceptor
│   ├─ apiError.ts                  # ApiError class
│   └─ queryClient.ts               # QueryClient config (staleTime: 30s)
├─ data/
│   ├─ types/
│   │   └─ auth.dto.ts              # LoginRequestDTO, LoginResponseDTO
│   ├─ repositories/
│   │   └─ authRepository.ts        # login(), logout(), refresh()
│   └─ queries/
│       └─ authQueries.ts           # Query key factory
├─ pages/
│   ├─ login/                       # Feature: Login
│   │   ├─ types.ts                 # ILoginForm, loginSchema (Zod)
│   │   ├─ facades/
│   │   │   ├─ useLoginState.ts     # isLoading, error state
│   │   │   └─ useLogin.ts          # Action hook: validate → repo → store → navigate
│   │   ├─ components/
│   │   │   └─ LoginForm.tsx        # Form UI (inputs, validation, submit button)
│   │   ├─ constants/
│   │   │   └─ loginUI.ts           # Vietnamese labels, error messages
│   │   └─ LoginPage.tsx            # Page entry point
│   └─ error-pages.tsx              # ForbiddenPage, NotFoundPage
├─ stores/
│   └─ authStore.ts                 # Zustand: user, tokens, isAuthenticated, login/logout
├─ shared/
│   ├─ components/
│   │   └─ ui/                      # shadcn/ui primitives (button, input, card, etc.)
│   ├─ context/
│   │   └─ toast-provider.tsx       # Sonner toast abstraction
│   ├─ guards/
│   │   └─ AuthGuard.tsx            # Route guard — redirects /dang-nhap if unauthenticated
│   ├─ layouts/
│   │   └─ AuthLayout.tsx           # Minimal layout for auth pages
│   └─ utils/
│       ├─ cn.ts                    # clsx + tailwind-merge
│       ├─ case.ts                  # snakeToCamelObj, camelToSnakeObj
│       ├─ format.ts                # formatPrice, formatDate, etc.
│       └─ index.ts                 # Label helpers (Vietnamese)
├─ App.tsx                          # Providers (QueryClient, Toast, Router)
├─ AppRoutes.tsx                    # Route definitions
└─ main.tsx                         # Entry point
```

## Naming Conventions

| Concept | Pattern | Example |
|---|---|---|
| UI Types | `I<Name>` | `ILoginForm` |
| DTO Types | `<Name>DTO` | `LoginRequestDTO` |
| State Hook | `use<Feature>State` | `useLoginState` |
| Action Hook | `use<Action><Feature>` | `useLogin` |
| Repository | `<name>Repository` | `authRepository` |
| Query Keys | `<name>Queries` | `authQueries` |
| Page Component | `<Name>Page` | `LoginPage` |
| Zod Schema | `camelCase` | `loginSchema` |

## Routing

```
/dang-nhap           → AuthLayout → LoginPage
/quen-mat-khau       → AuthLayout → ForgotPasswordPage
/dat-lai-mat-khau    → AuthLayout → ResetPasswordPage
/                     → DashboardLayout → DashboardPage
*                    → NotFoundPage
```

Routes requiring authentication are wrapped in `<AuthGuard>`, which reads `authStore.isAuthenticated` and redirects to `/dang-nhap` if false.

## Login Data Flow

```
LoginForm.tsx (View)
  ├─ reads: useLoginState() → { isLoading, error }
  └─ calls: useLogin() → mutate({ username, password, rememberMe })

useLogin.ts (Action hook)
  1. validate form data against loginSchema (Zod)
  2. get device token from localStorage
  3. authRepository.login(payload, deviceToken)
  4. onSuccess: authStore.login(tokens) → navigate("/")
  5. onError: map ApiError type → return structured error to View
     - 422 Validation → fieldErrors[]
     - 401 Invalid credentials → credentialError
     - 403 Device mismatch → deviceError
     - Network failure → networkError
  6. Side effects (navigate, toast) stay in hook — View never calls them

authRepository.ts (Data)
  1. camelToSnakeObj on request payload
  2. POST /auth/login with X-Device-Token header
  3. snakeToCamelObj on response → LoginResponseDTO
  4. Throws ApiError on failure
```

## Auth State Management

### 401 Handling

On 401 response, `httpClient.ts`'s response interceptor calls:

```
authStore.getState().logout()
```

This clears `authStore` (tokens + user) and `localStorage`. The `AuthGuard` component detects `isAuthenticated === false` and redirects via React Router — no hard page reload.

### Token Refresh (future)

When token refresh is needed:
1. 401 interceptor attempts `POST /auth/refresh` once
2. On success: update `authStore`, retry original request
3. On failure: call `authStore.logout()`, redirect to `/dang-nhap`

## Coding Standards

- Max ~200 lines per file; split at ~100 lines JSX for components
- One action hook per mutation
- Early returns / guard clauses over nested `if`
- NEVER use `useState`/`useReducer` in page components
- NEVER import DTO types in View
- NEVER call `httpClient` outside `platform/`
- Call `mutate(data)` unconditionally from View — guards in facade only
- Mutation side effects (navigate, toast) belong exclusively in action hooks
- `@/` alias for all cross-directory imports
- Relative imports only for `./` (same dir) or `../` (parent)
- All shared/reusable components in `shared/components/`
