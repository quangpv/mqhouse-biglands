# Frontend Implementation Plan

## Existing Setup (already done — no changes needed)

| Item | Status |
|---|---|
| Tailwind CSS v4 | ✅ `@tailwindcss/vite` plugin in `vite.config.ts`, `@import "tailwindcss"` in `index.css` |
| CSS variables (theme) | ⚠️ `oklch` defaults — needs alignment with `docs/screens/index.html` design tokens (hex colors, border-radius, shadows, Inter font, typography utilities, scrollbar) |
| `components.json` | ✅ v1 schema, `new-york` style, aliases `@/shared/components/ui` |
| `dark` mode variant | ✅ `@custom-variant dark (&:is(.dark *))` in `index.css` |
| Dependencies | ✅ `tailwindcss`, `tailwind-merge`, `cva`, `clsx`, `lucide-react`, `radix-ui` all installed |
| Toast context | ✅ `ToastProvider` exists in `shared/context/toast-provider.tsx` but imports `@/shared/components/ui/sonner` (doesn't exist yet) |

**Gap**: `shared/components/ui/` is empty — no shadcn component files exist. All must be created.

## Architecture

**View → Facade → Data → Platform** — three-layer strict dependency flow.

No Zustand for auth. Auth state is managed by:
- `authRepository` — token persistence (localStorage) + API calls
- React Query — user profile caching
- AuthGuard — reads tokens, renders or redirects

## Dependency Graph

```
Phase 0 (Foundation)                 Phase 1 (Login Feature)
─────────────────────                ─────────────────────
F0.0 index.css + index.html ─┐      F1.1 loginUI.constants
   theme customization       │
                              │
F0.1 auth.dto.ts ─┐          │      F1.2 types.ts ──────────┐
                  ├→ F0.2 ───┤                             │
F0.1 (types) ────┘  authRepo.│                             │
                     .ts      │                             │
                              │                             │
F0.2 (getAccessToken) ─→ F0.3 ├─→ F1.3 authQueries.ts      │
                     update    │                             │
                     http-cli. │                             │
                              │                             │
F0.2 (getAccessToken) ─→ F0.4 ├→ F1.4 useLoginState.ts     │
                     AuthGuard │         ← F1.3             │
                              │                             │
F0.5 AuthLayout.tsx           │         F1.5 useLogin.ts ←──┤
                              │    ← F0.2, F1.2, F1.3       │
F0.6 AppRoutes.tsx ← F0.4,   │                             │
                     F0.5 ───┤         F1.6 LoginForm.tsx ←─┤
                              │    ← F1.1, F1.2, F1.4, F1.5  │
F0.7 update App.tsx ← F0.6   │                              │
                              │    F1.7 LoginPage.tsx ← F1.6 │
F0.8 shadcn/ui primitives     │                              │
    (parallel to F0.1–F0.7)   │    F1.8 wire route ← F1.7,  │
                                        F0.6                │
```

**Rule**: Phase 0 must complete before Phase 1 starts. Phase 0 files are frozen after implementation — Login feature must NOT modify them.

## Phase 0 — Foundation (frozen after implementation)

### F0.0 — Theme customization: `index.css` + `index.html`

**Source**: `docs/screens/index.html` — extract design tokens.

**Changes to `frontend/index.css`**:
1. Replace all `oklch` CSS variable values with the design's hex values (approach 1 — direct replacement)
2. Add `--radius-card`, `--radius-button`, `--radius-input`, `--radius-modal` in `:root`
3. Add `--shadow-soft` in `:root`
4. Add `--color-success` and `--color-warning` to `@theme inline`
5. Add `--font-sans` to `@theme inline` pointing to Inter
6. Add custom `@utility` blocks for typography: `text-h1` (26px/700/1.2), `text-h2` (20px/600/1.25), `text-h3` (16px/600/1.3), `text-body` (13px/400/1.45), `text-small` (11px/400/1.4)
7. Add `::-webkit-scrollbar` styling
8. Add `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');` at top of file
9. Set `body { font-family: "Inter", sans-serif; }` in base layer

**Design token mapping**:

| shadcn var | Design hex |
|---|---|
| `--background` | `#F8FAFC` |
| `--foreground` | `#0F172A` |
| `--card` | `#FFFFFF` |
| `--card-foreground` | `#0F172A` |
| `--popover` | `#FFFFFF` |
| `--popover-foreground` | `#0F172A` |
| `--primary` | `#2563EB` |
| `--primary-foreground` | `#FFFFFF` |
| `--secondary` | `#F1F5F9` |
| `--secondary-foreground` | `#0F172A` |
| `--muted` | `#F1F5F9` |
| `--muted-foreground` | `#64748B` |
| `--accent` | `#F1F5F9` |
| `--accent-foreground` | `#0F172A` |
| `--destructive` | `#DC2626` |
| `--destructive-foreground` | `#FFFFFF` |
| `--border` | `#E2E8F0` |
| `--input` | `#E2E8F0` |
| `--ring` | `#2563EB` |

**Changes to `frontend/index.html`**:
- Add `<title>CRM Bất động sản</title>`
- Add Inter Google Fonts link in `<head>`
- Set `<html lang="vi">`
- Change `<link rel="icon">` if favicon exists

### F0.1 — `data/types/auth.dto.ts`

DTO types matching API contract exactly:
- `LoginRequestDTO`: `{ username: string; password: string }`
- `LoginResponseDTO`: `{ access_token: string; refresh_token: string }`
- `UserDTO`: full User object from API (`id`, `full_name`, `username`, `phone`, `email`, `role`, `is_active`, `device_limit_enabled`, `organization_id`, `organization`, `property_type_ids`, `transaction_type_ids`, `notification_prefs`, `created_at`)
- `UserRole`: `"sale" | "approver" | "admin"`

Pure types, zero logic, no imports outside `data/types/`.

### F0.2 — `data/repositories/authRepository.ts`

**Token persistence** (localStorage helpers):
- `getAccessToken(): string | null`
- `getRefreshToken(): string | null`
- `setTokens(access: string, refresh: string): void`
- `clearTokens(): void`

**API operations**:
- `login(payload: LoginRequestDTO, deviceToken?: string): Promise<LoginResponseDTO>`
  - `camelToSnakeObj` on request
  - `POST /auth/login` with optional `X-Device-Token` header
  - `snakeToCamelObj` on response
- `getProfile(): Promise<UserDTO>`
  - `GET /me`
  - `snakeToCamelObj` on response
- `logout(): Promise<void>`
  - `POST /auth/logout`
- `refresh(token: string): Promise<LoginResponseDTO>`
  - `POST /auth/refresh`

**Rules**:
- Import `httpClient` from `@/platform/http-client`
- Import `camelToSnakeObj` / `snakeToCamelObj` from `@/shared/utils/case`
- NEVER import UI types or View code

### F0.3 — Update `platform/http-client.ts`

**Changes**:
1. Request interceptor: `const token = authRepository.getAccessToken()` instead of `localStorage.getItem("auth-token")`
2. Error interceptor: on 401, `authRepository.clearTokens()` then `window.location.href = "/dang-nhap"`
3. Import `authRepository` from `@/data/repositories/auth-repository`

### F0.4 — `shared/guards/AuthGuard.tsx`

**Behavior**:
- `authRepository.getAccessToken()`:
  - `null` or `undefined` → `<Navigate to="/dang-nhap" replace />`
  - Present → render `<Outlet />`
- Wraps dashboard/authenticated routes

### F0.5 — `shared/layouts/AuthLayout.tsx`

Centered layout for auth pages:
- Full-viewport flex container
- Card with logo area, `<Outlet />`, footer
- Matches `login_content.html` design: blue accent `#2563EB`, rounded card, shadow

### F0.6 — `AppRoutes.tsx`

Route tree:
```
<Routes>
  <Route element={<AuthLayout />}>
    <Route path="/dang-nhap" element={<LoginPage />} />
  </Route>
  <Route element={<AuthGuard />}>
    <Route path="/" element={<DashboardPage />} />
  </Route>
  <Route path="/403" element={<ForbiddenPage />} />
  <Route path="*" element={<NotFoundPage />} />
</Routes>
```

### F0.7 — Update `App.tsx`

Replace empty `<BrowserRouter>` with `ToastProvider` + `AppRoutes`:
```
QueryClientProvider → BrowserRouter → ToastProvider → AppRoutes
```

### F0.8 — Create shadcn/ui primitives

`shared/components/ui/` is empty. Five files needed, matching existing CSS variables + `components.json` aliases. The existing `ToastProvider` imports `sonner.tsx` — app won't build without it.

| File | What it exports | Key deps |
|---|---|---|
| `button.tsx` | `Button` with variants + sizes via `cva()` | `cva`, `cn` |
| `input.tsx` | `Input` with `forwardRef` | `cn` |
| `label.tsx` | `Label` with `@radix-ui/react-label` | `@radix-ui/react-label` (incl. in `radix-ui` package) |
| `card.tsx` | `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` | `cn` |
| `sonner.tsx` | `Toaster` — wraps sonner's `<Toaster />` | `sonner`, `useTheme` from `next-themes` |

**Rules**:
- Use `cn()` from `@/shared/utils/cn` for class merging
- Reference `index.css` CSS variables (`--primary`, `--border`, `--input`, `--ring`, `--radius`, etc.)
- No custom CSS or PostCSS config changes needed — Tailwind v4 + CSS variables are fully set up
- F0.8 has zero dependencies — can run in parallel with F0.1–F0.7

## Phase 1 — Login Feature

### F1.1 — `pages/login/constants/loginUI.ts`

Vietnamese labels + error messages as const objects:
- `LOGIN_LABELS`: welcomeBack, subtitle, username/password labels/placeholders, rememberMe, forgotPassword, signIn, signingIn, noAccount, contactAdmin
- `LOGIN_ERRORS`: required, invalidCredentials, networkError, connectionFailed

### F1.2 — `pages/login/types.ts`

UI types + Zod schema:
- `ILoginForm`: `{ username: string; password: string; rememberMe: boolean }`
- `ILoginError`: `{ fieldErrors?: Record<string, string>; credentialError?: string; networkError?: string }`
- `loginSchema`: Zod — username `min(1).max(100)`, password `min(1)`, rememberMe `boolean`
- Import `LOGIN_ERRORS` from constants

### F1.3 — `data/queries/authQueries.ts`

Query key factory + hooks:
- `authQueries.me` — key for profile query
- `useProfileQuery()`: `useQuery(authQueries.me, authRepository.getProfile, { enabled, staleTime: 5min })`

### F1.4 — `pages/login/facades/useLoginState.ts`

State hook — exposes to View:
- `isLoading: boolean`
- `error: ILoginError | null`
- Reads from React Query mutation state internally
- Maps error types to `ILoginError`:
  - `400/422` → `fieldErrors`
  - `401` → `credentialError`
  - `403` → `deviceError`
  - Network → `networkError`

**Rules**:
- NEVER import action hooks
- NEVER import DTOs or repositories

### F1.5 — `pages/login/facades/useLogin.ts`

Action hook — single mutation:
1. Validate form against `loginSchema`
2. Get device token from `localStorage` key `device-token`
3. `authRepository.login(payload, deviceToken)`
4. On success:
   - `authRepository.setTokens(res.accessToken, res.refreshToken)`
   - `queryClient.invalidateQueries(authQueries.me)`
   - `useNavigate()("/")`
5. On error: return structured `ILoginError`, NEVER rethrow

**Rules**:
- Single `useMutation` — one action per hook
- Side effects (navigate, invalidate) EXCLUSIVELY in this hook
- View calls `mutate(data)` unconditionally

### F1.6 — `pages/login/components/LoginForm.tsx`

**Screen States**:

| State | UI |
|---|---|
| Idle | Clean form, fields, submit button, forgot-password link, remember-me checkbox |
| Loading | Spinner on button, "Đang đăng nhập...", fields disabled |
| Field Validation | Red border + error message below field, clears on input |
| Invalid Credentials | Red inline banner above submit: "Tên đăng nhập hoặc mật khẩu không đúng" |
| Network Error | Red banner at top: "Không thể đăng nhập. Vui lòng thử lại." |

- `react-hook-form` + `zodResolver(loginSchema)`
- shadcn/ui `Card`, `Input`, `Button`
- lucide-react: `Layers`, `AlertCircle`, `AlertTriangle`, `ShieldAlert`, `LoaderCircle`
- NEVER `useState`/`useReducer`
- NEVER import DTOs or repositories

### F1.7 — `pages/login/LoginPage.tsx`

Minimal page shell:
```tsx
export default function LoginPage() {
  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  )
}
```

Zero logic.

### F1.8 — Wire `/dang-nhap` in `AppRoutes.tsx`

Add import + route:
```tsx
import LoginPage from "@/pages/login/LoginPage"
// <Route path="/dang-nhap" element={<LoginPage />} />
```

## Auth Flow Summary

```
Login
  useLogin.ts
    → authRepository.login(payload, deviceToken)    ← API
    → authRepository.setTokens(access, refresh)      ← localStorage
    → queryClient.invalidateQueries(authQueries.me)  ← refetch user
    → navigate("/")

Page Refresh
  AuthGuard.tsx
    → authRepository.getAccessToken()?
      YES → render Outlet, useProfileQuery() fetches user
      NO  → redirect /dang-nhap

Expired Token
  http-client.ts 401 interceptor
    → authRepository.clearTokens()
    → window.location.href = "/dang-nhap"
```

## Coding Standards

- Max ~200 lines per file; split at ~100 lines JSX for components
- One action hook per mutation
- Early returns / guard clauses over nested if
- NEVER `useState`/`useReducer` in page components
- NEVER import DTO types in View
- NEVER call `httpClient` outside `platform/`
- Call `mutate(data)` unconditionally from View — guards in facade only
- Mutation side effects (navigate, toast) exclusively in action hooks
- `@/` alias for cross-directory imports, relative for `./` or `../`
- File naming: `kebab-case.ts`, `PascalCase.tsx` for components

## Verification

- [ ] `npm run build` passes
- [ ] No DTOs in `pages/login/components/` or `pages/login/LoginPage.tsx`
- [ ] No `useState`/`useReducer` in View
- [ ] `authRepository` is the sole source of token read/write
- [ ] No Zustand import exists for auth
- [ ] Foundation files untouched after Phase 1 starts
