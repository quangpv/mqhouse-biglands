# Frontend Architecture

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | React 19 + TypeScript (~6.0.2) | Component framework |
| Build | Vite 8 | Dev server + bundler |
| Routing | react-router-dom v7 | SPA navigation |
| Server State | TanStack React Query v5 | Caching, fetching, mutations |
| Client State | Zustand v5 | Sidebar state, UI preferences |
| HTTP | Axios 1.18 | API client |
| Forms | React Hook Form v7 + Zod v4 | Form state + validation |
| Styling | Tailwind CSS v4 + shadcn/ui | Utility-first CSS + primitives |
| Icons | Lucide React | Icon library |
| Toasts | Sonner | Toast notifications |
| Dates | date-fns | Date formatting/manipulation |
| Image Compression | browser-image-compression | Client-side image compression to WebP |
| Date Picker | react-day-picker | Calendar/date selection |
| Carousel | embla-carousel-react | Image gallery carousel |
| Themes | next-themes | Theme switching |

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
  → Facade action hook (catches, fires toast)
  → View (shows retry UI if needed)
```

## File Naming Conventions

| Layer | Convention | Examples |
|---|---|---|
| Platform files | `kebab-case.ts` | `http-client.ts`, `api-error.ts`, `token.ts` |
| Repository files | `kebab-case.ts` | `auth-repository.ts`, `user-repository.ts` |
| Query files | `camelCase.ts` | `authQueries.ts`, `propertyQueries.ts` |
| DTO files | `kebab-case.dto.ts` | `auth.dto.ts`, `property.dto.ts` |
| Hook files | `camelCase.ts` | `useLogin.ts`, `useHomeState.ts` |
| Component files | `PascalCase.tsx` | `LoginForm.tsx`, `Sidebar.tsx` |
| UI type interfaces | `I<Name>` | `ILoginForm`, `IUser` |
| Zod schemas | `camelCase` | `loginSchema` |

## Project Structure

```
src/
├─ platform/
│   ├─ http-client.ts              # Axios instance with auth interceptor
│   ├─ api-error.ts                # ApiError class
│   ├─ query-client.ts             # QueryClient config (staleTime: 30s)
│   └─ token.ts                    # localStorage token management
├─ data/
│   ├─ types/                      # 17 DTO files
│   │   ├─ auth.dto.ts
│   │   ├─ property.dto.ts
│   │   ├─ approval.dto.ts
│   │   ├─ user.dto.ts
│   │   ├─ notification.dto.ts
│   │   ├─ file.dto.ts
│   │   ├─ organization.dto.ts
│   │   ├─ review.dto.ts
│   │   ├─ hot.dto.ts
│   │   ├─ pin.dto.ts
│   │   ├─ tag.dto.ts
│   │   ├─ transaction-type.dto.ts
│   │   ├─ property-type.dto.ts
│   │   ├─ geography.dto.ts
│   │   ├─ master-data.dto.ts
│   │   ├─ supports.dto.ts
│   │   └─ backfill.dto.ts
│   ├─ repositories/               # 17 repository files (kebab-case)
│   │   ├─ auth-repository.ts
│   │   ├─ property-repository.ts
│   │   ├─ approval-repository.ts
│   │   ├─ user-repository.ts
│   │   ├─ notification-repository.ts
│   │   ├─ file-repository.ts
│   │   ├─ organization-repository.ts
│   │   ├─ review-repository.ts
│   │   ├─ hot-repository.ts
│   │   ├─ pin-repository.ts
│   │   ├─ tag-repository.ts
│   │   ├─ transaction-type-repository.ts
│   │   ├─ property-type-repository.ts
│   │   ├─ geography-repository.ts
│   │   ├─ master-data-repository.ts
│   │   ├─ support-repository.ts
│   │   └─ backfill-repository.ts
│   └─ queries/                    # 12 query key factories
│       ├─ authQueries.ts
│       ├─ propertyQueries.ts
│       ├─ approvalQueries.ts
│       ├─ userQueries.ts
│       ├─ notificationQueries.ts
│       ├─ organizationQueries.ts
│       ├─ reviewQueries.ts
│       ├─ geographyQueries.ts
│       ├─ tagQueries.ts
│       ├─ transactionTypeQueries.ts
│       ├─ propertyTypeQueries.ts
│       └─ supportQueries.ts
├─ pages/
│   ├─ home/                       # Property listing + hot carousel
│   │   ├─ components/             # FilterPanel, ProductCard, ProductGrid, HotProductSection, etc.
│   │   ├─ facades/                # useHomeState, usePinProperty, usePromoteToHot, etc.
│   │   └─ HomePage.tsx
│   ├─ cart/                       # My listed properties
│   │   ├─ components/             # Reuses home components
│   │   └─ CartPage.tsx
│   ├─ approvals/                  # Approval workflow
│   │   ├─ components/             # ApproveDialog, RejectDialog
│   │   ├─ facades/                # useApprovalsState, useApproveApproval, useRejectApproval
│   │   └─ ApprovalsPage.tsx
│   ├─ notification/               # Notification center
│   │   ├─ components/             # NotificationList, NotificationFilters
│   │   ├─ facades/                # useNotificationState, useMarkReadNotification
│   │   └─ NotificationPage.tsx
│   ├─ create-product/             # Product creation + editing
│   │   ├─ components/             # BasicInfoSection, LocationSection, MediaSection, etc.
│   │   ├─ facades/                # useCreateProductState, useSaveProduct, useProductFormMapper
│   │   └─ CreateProductPage.tsx
│   ├─ product-details/            # Product detail view
│   │   ├─ components/             # ProductGallery, StatusLogSection, TransitionDialog, etc.
│   │   ├─ facades/                # useProductDetailsState, useProductDetailsMapper
│   │   └─ ProductDetailsPage.tsx
│   ├─ user-management/            # Admin user CRUD
│   │   ├─ components/             # UsersTable, UserFormDialog, ChangeUserPasswordDialog, etc.
│   │   ├─ facades/                # useUserManagementState, useCreateUser, useUpdateUser, etc.
│   │   └─ UserManagementPage.tsx
│   ├─ user-profile/               # Personal profile
│   │   ├─ components/             # ProfileInfoCard, ProfileSecurityCard, etc.
│   │   └─ UserProfilePage.tsx
│   ├─ system-config/              # System configuration (5 sub-features)
│   │   ├─ components/             # SystemConfigTabs
│   │   ├─ transaction-types/      # CRUD: TransactionTypesTab, TransactionTypeFormDialog
│   │   ├─ tags/                   # CRUD: TagsTab, TagFormDialog
│   │   ├─ organizations/          # CRUD: OrganizationsTab, OrganizationFormDialog
│   │   ├─ property-types/         # CRUD components + facades
│   │   ├─ backfill/               # Search tools: BackfillCard, SearchCheckCard
│   │   └─ SystemConfigPage.tsx
│   ├─ forgot-password/            # Forgot + reset password
│   │   └─ ForgotPasswordPage.tsx, ResetPasswordPage.tsx
│   ├─ placeholder/                # ComingSoonPage
│   └─ index.ts                    # Barrel: ForbiddenPage, NotFoundPage
├─ shared/
│   ├─ components/
│   │   ├─ ui/                     # 24 shadcn/ui primitives
│   │   ├─ layout/                 # Sidebar, Topbar, NotificationDropdown, UserDropdown, etc.
│   │   └─ common/                 # ResourceShell, GenericResourceTab, ConfirmDeleteDialog, etc.
│   ├─ hooks/                      # 10 shared hooks
│   ├─ constants/                  # approvalsUI, statusLabels
│   ├─ types/                      # filterTypes
│   ├─ image/                      # validateImage
│   ├─ guards/                     # ProtectedRoute, RedirectIfAuth
│   ├─ layouts/                    # MainLayout, AuthLayout
│   └─ utils/                      # formatPrice, formatDate, getStatusColor, etc.
├─ App.tsx                         # Providers (QueryClient, Toast, Router)
├─ AppRoutes.tsx                   # Route definitions
└─ main.tsx                        # Entry point
```

## Auth Architecture

Auth state is managed via **TanStack Query + localStorage tokens** (no Zustand store).

### Token Management (`platform/token.ts`)
- `getAccessToken()` / `getRefreshToken()` — read from localStorage
- `setTokens(access, refresh)` — write both tokens
- `clearTokens()` — remove both tokens
- `getDeviceToken()` — read device token for login

### Auth State Flow
```
useProfileQuery() → GET /me → IUser | null
  ↓
useAuthState() → { user, isLoading, isAuthenticated }
  ↓
View components read auth state from facade
```

### Guards
- `ProtectedRoute` — wraps authenticated routes, checks `getAccessToken()`, redirects to `/dang-nhap` if missing
- `RedirectIfAuth` — wraps auth pages, redirects to `/` if already authenticated

### 401 Handling
```
httpClient response interceptor (401)
  → clearTokens() from platform/token.ts
  → window.location.href = "/dang-nhap" (hard reload)
```

## Routing

```
ProtectedRoute (checks getAccessToken()):
  MainLayout:
    /                       → HomePage
    /gio-hang               → CartPage
    /phe-duyet              → ApprovalsPage
    /thong-bao              → NotificationPage
    /tao-hang-moi           → CreateProductPage
    /sua-bat-dong-san/:id   → CreateProductPage (edit mode)
    /bat-dong-san/:id       → ProductDetailsPage
    /quan-ly-nguoi-dung     → UserManagementPage
    /ho-so-ca-nhan          → UserProfilePage
    /cau-hinh-he-thong      → SystemConfigPage

RedirectIfAuth (redirects to / if authenticated):
    /dang-nhap              → AuthLayout → LoginPage
    /quen-mat-khau          → AuthLayout → ForgotPasswordPage
    /dat-lai-mat-khau       → AuthLayout → ResetPasswordPage
    /reset-password         → AuthLayout → ResetPasswordPage

/403                       → ForbiddenPage
*                          → NotFoundPage
```

## Layout System

### MainLayout
Full app shell for authenticated pages:
- `Sidebar` — responsive, static nav items + dynamic approval groups from API
- `Topbar` — sticky, page title, notification dropdown, user dropdown
- `<Outlet/>` — page content
- `ScrollRestoration`
- Initializes WebSocket connection via `useWebSocket()`
- Manages logout and change-password modals

### AuthLayout
Minimal layout for login/forgot-password/reset-password pages with footer.

## Sidebar Navigation

Dynamic from API with role-based filtering:
- **Static nav items**: Trang chu, Gio hang, Thong bao, Quan ly nguoi dung, Cau hinh he thong
- **Dynamic approval groups**: Fetched from `useTransactionTypesQuery()` — each transaction type becomes an expandable nav group with 5 sub-tabs
- **Role filtering**: ADMIN sees all; APPROVER sees approval groups; SALE sees only static items
- **Badge counts**: From `useNotificationCountsQuery` and `useApprovalCountsQuery`
- **State**: Zustand store (`useSidebarStore`) for mobile open/close and expanded state

## WebSocket Pattern

`useWebSocket()` hook (initialized in MainLayout):
- Connects to `ws(s)://{host}/api/ws?token={accessToken}`
- Auto-reconnects every 3 seconds on disconnect
- On `notification_created` events: invalidates `notificationKeys.all`, `propertyKeys.all`, `approvalKeys.all`
- Returns `{ isConnected }` for UI status

## Shared Hooks

| Hook | Purpose |
|---|---|
| `useWebSocket` | Real-time WebSocket with auto-reconnect, query invalidation |
| `useSidebar` / `useSidebarStore` | Sidebar nav with dynamic items, role-based filtering, badge counts |
| `useTopBarState` | Dynamic page title resolution from nav items |
| `usePagination` | Client-side array pagination |
| `useServerPagination` | Server-side pagination next/prev helpers |
| `useDebounce` | Debounced value (default 1000ms) |
| `useModal` / `useDeleteModal` | Modal open/close + edit target state |
| `useAddressLookup` | Geography ID-to-name resolution |
| `useFilterOptions` | Aggregated filter options from multiple queries |
| `useNotificationDropdown` | Notification dropdown data (unread count + recent) |

## Data Layer

### Repositories (17 files)
Each repository wraps Axios calls with camelCase→snake_case conversion:

| Repository | Endpoints |
|---|---|
| `authRepository` | login, refresh, logout, changePassword, forgotPassword, resetPassword |
| `propertyRepository` | CRUD, transitions, status-logs, counts, pending-approval |
| `approvalRepository` | list, detail, approve, reject, counts |
| `userRepository` | CRUD, deactivate, reactivate, resetPassword, resetDevice, changePassword |
| `notificationRepository` | list, counts, markRead, markAllRead |
| `fileRepository` | upload, get, delete |
| `organizationRepository` | CRUD |
| `reviewRepository` | list, detail, create, delete |
| `hotRepository` | list, promote, remove |
| `pinRepository` | add, remove |
| `tagRepository` | CRUD |
| `transactionTypeRepository` | CRUD |
| `propertyTypeRepository` | CRUD |
| `geographyRepository` | provinces, districts, wards |
| `masterDataRepository` | getMasterData |
| `supportRepository` | getSupport |
| `backfillRepository` | backfill, checkSearch |

### Query Key Factories (12 files)
Each domain has a query key factory for cache invalidation:
```typescript
// Example: propertyQueries.ts
export const propertyKeys = {
  all: ['properties'] as const,
  lists: () => [...propertyKeys.all, 'list'] as const,
  list: (filters) => [...propertyKeys.lists(), filters] as const,
  details: () => [...propertyKeys.all, 'detail'] as const,
  detail: (id) => [...propertyKeys.details(), id] as const,
}
```

### DTO Types (17 files)
Each DTO maps 1:1 to backend response schemas. Naming: `I<Name>` for UI types, `<Name>DTO` for wire format.

## Coding Standards

- Max ~200 lines per file; split at ~100 lines JSX for components
- One action hook per mutation
- Early returns / guard clauses over nested `if`
- NEVER import DTO types in View layer
- NEVER call `httpClient` outside `platform/`
- Call `mutate(data)` unconditionally from View — guards in facade only
- Mutation side effects (navigate, toast) belong exclusively in action hooks
- `@/` alias for all cross-directory imports
- Relative imports only for `./` (same dir) or `../` (parent)
- All shared/reusable components in `shared/components/`
- Mapper hooks transform DTOs to UI types (never in View)
