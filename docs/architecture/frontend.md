# Frontend Architecture — Biglands

> **Skill**: `simple-frontend-dev`(.ai/skills/frontend-dev) — React/TypeScript, View → Facade → Data  
> **Source Documents**: openapi.yaml, domain-model.md, business-spec.md, screens/, user-flows/  
> **Status**: Design reference — no implementation

---

## 1. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | TypeScript 5.x |
| Framework | React 18+ |
| Build tool | Vite |
| Styling | TailwindCSS |
| Server state | TanStack Query v5 |
| Client state | Zustand |
| Forms | React Hook Form + Zod resolver |
| Validation | Zod schemas |
| UI components | shadcn/ui (Radix primitives) |
| Icons | Lucide |
| HTTP client | Axios |
| Testing | Vitest + Playwright |
| Path alias | `@/` → `src/` |

## 2. Project Structure

```
src/
├── main.tsx                              # Entry point
├── App.tsx                               # Router + AuthProvider + QueryClientProvider
├── AppRoutes.tsx                         # Route definitions + guards
├── index.css                             # Tailwind directives
│
├── data/                                 # DATA LAYER
│   ├── infra/
│   │   ├── httpClient.ts                 # Axios instance, interceptors, token injection, error normalizer
│   │   ├── queryClient.ts                # TanStack Query client + default options
│   │   └── apiError.ts                   # Normalized ApiError type + error code enum
│   ├── repositories/
│   │   ├── authRepository.ts             # login(), logout(), getMe()
│   │   ├── listingRepository.ts          # CRUD + submit/withdraw + browse/search + uploadImage
│   │   ├── dealEventRepository.ts        # deposit/closure/cancellation/sold-out
│   │   ├── approvalRepository.ts         # queues, approve, reject, bulk
│   │   ├── notificationRepository.ts     # list, unreadCount, markRead, markAllRead
│   │   ├── userRepository.ts             # CRUD, deactivate, reactivate, assignRole
│   │   ├── pinRepository.ts              # pin, unpin, listMyPins
│   │   ├── hotProductRepository.ts       # promote, unpromote, reorder
│   │   └── geographyRepository.ts        # getCities, getDistricts, getWards
│   ├── types/                            # One file per domain — DTOs only
│   │   ├── auth.dto.ts
│   │   ├── listing.dto.ts
│   │   ├── dealEvent.dto.ts
│   │   ├── approval.dto.ts
│   │   ├── notification.dto.ts
│   │   ├── user.dto.ts
│   │   ├── pin.dto.ts
│   │   ├── geography.dto.ts              # CityDTO, DistrictDTO, WardDTO
│   │   └── common.dto.ts                 # Pagination, ApiError, enums
│   ├── queries/                          # Query key factories
│   │   ├── listingQueries.ts
│   │   ├── approvalQueries.ts
│   │   ├── notificationQueries.ts
│   │   ├── userQueries.ts
│   │   └── geographyQueries.ts           # geographyKeys.all, cities, districts, wards
│   └── utils/
│       └── serializers.ts                # Transform snake_case ↔ camelCase
│
├── pages/                                # FEATURE MODULES
│   ├── auth/                             # Login
│   │   ├── facades/
│   │   │   ├── useLoginState.ts          # State hook: owns login form (RHF + Zod)
│   │   │   └── useLogin.ts              # Action hook: login mutation
│   │   ├── components/
│   │   │   └── LoginForm.tsx
│   │   ├── types.ts                      # IAuthState, ILoginForm
│   │   └── LoginPage.tsx
│   │
│   ├── shared-cart/                      # Home — browse all listings
│   │   ├── facades/
│   │   │   ├── useSharedCartState.ts     # State hook: listings, filters, pagination, pins, search
│   │   │   └── usePinListing.ts          # Action hook: toggle pin
│   │   ├── hooks/
│   │   │   └── useListingMapper.ts       # DTO ↔ IListingCard
│   │   ├── components/
│   │   │   ├── ListingGrid.tsx
│   │   │   ├── ListingCard.tsx
│   │   │   ├── HotProductStrip.tsx
│   │   │   ├── FilterTabs.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   └── Pagination.tsx
│   │   ├── constants/
│   │   │   └── listingUI.ts              # Status labels, filter options, Vietnamese text
│   │   ├── types.ts                      # IListingCard, IFilterTab, ISearchState
│   │   └── SharedCartPage.tsx
│   │
│   ├── product-detail/                   # Listing detail + deal actions
│   │   ├── facades/
│   │   │   ├── useProductDetailState.ts  # State hook: listing detail + deal action forms
│   │   │   ├── useReportDeposit.ts       # Action hook: report deposit
│   │   │   ├── useReportClosure.ts       # Action hook: report closure
│   │   │   ├── useReportCancellation.ts  # Action hook: report cancellation
│   │   │   └── useReportSoldOut.ts       # Action hook: report sold-out
│   │   ├── hooks/
│   │   │   └── useProductDetailMapper.ts
│   │   ├── components/
│   │   │   ├── ImageGallery.tsx
│   │   │   ├── KeyInfoSection.tsx
│   │   │   ├── DealActionButtons.tsx
│   │   │   ├── PropertyFeaturesTable.tsx
│   │   │   ├── ReviewsSection.tsx
│   │   │   └── AgentContactInfo.tsx
│   │   ├── types.ts                      # IProductDetail, IDealAction
│   │   └── ProductDetailPage.tsx
│   │
│   ├── listing-form/                     # Create + Edit (shared form module)
│   │   ├── facades/
│   │   │   ├── useListingFormState.ts    # State hook: owns form (RHF + Zod), mode flag
│   │   │   ├── useCreateListing.ts       # Action hook: create + upload images
│   │   │   └── useUpdateListing.ts       # Action hook: update
│   │   ├── components/
│   │   │   ├── BasicInfoSection.tsx      # Transaction type, property type, title, description
│   │   │   ├── PropertyDetailsSection.tsx# Price, area dimensions, rooms, floors, bathrooms
│   │   │   ├── LocationSection.tsx       # Wraps LocationCascade + street/house number
│   │   │   ├── CommissionSection.tsx     # Commission type + value
│   │   │   ├── ContactSection.tsx        # Owner phone
│   │   │   └── ImageUploader.tsx         # Upload, preview, remove, max 20 images
│   │   ├── types.ts                      # IListingForm, IListingFormMode, Zod schema
│   │   ├── CreateListingPage.tsx         # Route: /tin/tao-moi
│   │   └── EditListingPage.tsx           # Route: /tin/:id/chinh-sua
│   │
│   ├── my-cart/                          # User's own listings
│   │   ├── facades/
│   │   │   ├── useMyCartState.ts         # State hook: listings grouped by status
│   │   │   ├── useDeleteListing.ts       # Action hook: delete DRAFT
│   │   │   └── useWithdrawListing.ts     # Action hook: withdraw ACTIVE → DRAFT
│   │   ├── components/
│   │   │   ├── MyCartListingCard.tsx
│   │   │   ├── MyCartFilterTabs.tsx
│   │   │   └── ListingActions.tsx
│   │   ├── types.ts
│   │   └── MyCartPage.tsx
│   │
│   ├── my-cart-detail/                   # Owner's listing detail view
│   │   ├── facades/
│   │   │   └── useMyCartDetailState.ts
│   │   ├── components/
│   │   │   └── OwnerListingActions.tsx
│   │   ├── types.ts
│   │   └── MyCartDetailPage.tsx
│   │
│   ├── notifications/
│   │   ├── facades/
│   │   │   ├── useNotificationState.ts   # State hook: list, filters, pagination
│   │   │   ├── useMarkRead.ts            # Action hook: mark single as read
│   │   │   └── useMarkAllRead.ts         # Action hook: mark all as read
│   │   ├── hooks/
│   │   │   └── useNotificationMapper.ts
│   │   ├── components/
│   │   │   ├── NotificationFilterTabs.tsx
│   │   │   ├── NotificationItem.tsx
│   │   │   └── NotificationList.tsx
│   │   ├── types.ts
│   │   └── NotificationsPage.tsx
│   │
│   ├── approval-queue/                   # Generic template — 15 queues
│   │   ├── facades/
│   │   │   ├── useApprovalQueueState.ts  # State hook: queue items, filters, selection
│   │   │   ├── useApproveItem.ts         # Action hook: approve single
│   │   │   ├── useRejectItem.ts          # Action hook: reject with reason form
│   │   │   └── useBulkApprove.ts         # Action hook: bulk approve
│   │   ├── hooks/
│   │   │   └── useApprovalMapper.ts
│   │   ├── components/
│   │   │   ├── QueueHeader.tsx
│   │   │   ├── QueueListingCard.tsx
│   │   │   ├── ApproveConfirmDialog.tsx
│   │   │   ├── RejectReasonDialog.tsx
│   │   │   └── BulkApproveBar.tsx
│   │   ├── constants/
│   │   │   └── queueUI.ts                # queueType → Vietnamese labels
│   │   ├── types.ts
│   │   └── ApprovalQueuePage.tsx         # Route: /admin/:txType/:queueType
│   │
│   ├── user-management/                  # Admin only
│   │   ├── facades/
│   │   │   ├── useUserListState.ts       # State hook: list, search, pagination
│   │   │   ├── useUserFormState.ts       # State hook: owns create/edit form (RHF + Zod)
│   │   │   ├── useCreateUser.ts          # Action hook
│   │   │   ├── useUpdateUser.ts          # Action hook
│   │   │   ├── useDeactivateUser.ts      # Action hook
│   │   │   └── useAssignRole.ts          # Action hook
│   │   ├── components/
│   │   │   ├── UserTable.tsx
│   │   │   ├── UserForm.tsx
│   │   │   └── UserActionDialogs.tsx
│   │   ├── types.ts
│   │   ├── UserListPage.tsx
│   │   └── UserFormPage.tsx
│   │
│   └── hot-products/                     # Admin only
│       ├── facades/
│       │   ├── useHotProductsState.ts    # State hook: hot list, drag state
│       │   ├── usePromoteToHot.ts        # Action hook
│       │   ├── useRemoveHot.ts           # Action hook
│       │   └── useReorderHot.ts          # Action hook
│       ├── components/
│       │   ├── HotProductList.tsx
│       │   ├── HotProductItem.tsx
│       │   └── AddHotProductDialog.tsx
│       ├── types.ts
│       └── HotProductsPage.tsx
│
├── shared/                               # SHARED LAYER
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── AppLayout.tsx             # TopBanner + Sidebar + Outlet
│   │   │   ├── Sidebar.tsx              # Role-aware sidebar with accordion menus
│   │   │   ├── TopBanner.tsx            # Notification bell + user dropdown
│   │   │   └── SidebarNavItem.tsx
│   │   ├── ui/                           # shadcn components (generated by CLI)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── input.tsx, select.tsx, textarea.tsx, label.tsx, form.tsx
│   │   │   ├── table.tsx
│   │   │   ├── pagination.tsx
│   │   │   ├── tabs.tsx, accordion.tsx
│   │   │   ├── sheet.tsx, popover.tsx
│   │   │   ├── avatar.tsx, skeleton.tsx, separator.tsx, scroll-area.tsx
│   │   │   └── sonner.tsx               # Toast system (replaces custom ToastContext)
│   │   ├── app/                          # Custom app-specific components
│   │   │   ├── EmptyState.tsx
│   │   │   ├── ErrorState.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── ConfirmDialog.tsx
│   │   │   └── SearchInput.tsx
│   │   └── icons/
│   ├── context/
│   │   └── AuthContext.tsx               # AuthProvider, useAuthContext
│   ├── hooks/
│   │   ├── useAuth.ts                    # Session state, role checks
│   │   ├── useRoleGuard.ts               # requireRole → redirect or 403
│   │   ├── useDebounce.ts
│   │   └── useRelativeTime.ts            # Vietnamese relative timestamps
│   ├── lib/
│   │   └── utils.ts                      # cn() — Tailwind class merging utility (shadcn convention)
│   └── utils/
│       ├── formatters.ts                 # Price (VND), area, date
│       └── validators.ts                 # Shared validation rules
│
├── stores/                               # Zustand stores
│   ├── authStore.ts                      # Token, currentUser, login/logout actions
│   └── uiStore.ts                        # Sidebar state, theme, global modals
│
└── styles/
    └── variables.css                     # CSS custom properties
```

## 3. Route Design

| Route | Screen | Page Component | Role |
|-------|--------|---------------|------|
| `/dang-nhap` | Login | `LoginPage` | Public |
| `/` | Shared Cart Home | `SharedCartPage` | AGENT+ |
| `/tin/:id` | Product Detail | `ProductDetailPage` | AGENT+ |
| `/gio-hang-chung` | My Cart | `MyCartPage` | AGENT+ |
| `/tin/tao-moi` | Create Listing | `CreateListingPage` | AGENT+ |
| `/tin/:id/chinh-sua` | Edit Listing | `EditListingPage` | Owner |
| `/thong-bao` | Notifications | `NotificationsPage` | AGENT+ |
| `/duyet/:queueType` | Approval Queue | `QueueListPage` | APPROVER+ |
| `/duyet/:queueType/:id` | Approval Detail | `QueueDetailPage` | APPROVER+ |
| `/tin-noi-bat` | Hot Products | `HotProductsPage` | ADMIN |
| `/nguoi-dung` | User List | `UserListPage` | ADMIN |
| `/nguoi-dung/tao-moi` | Create User | `CreateUserPage` | ADMIN |
| `/nguoi-dung/:id/chinh-sua` | Edit User | `EditUserPage` | ADMIN |

### Route params for approval queues

`/duyet/:queueType`

| Param | Values |
|-------|--------|
| `queueType` | `listing-post`, `deposit`, `closure`, `cancellation`, `sold-out` |

Queue items are filtered by transaction type via query parameter. A single `QueueListPage` handles all queues.

## 4. App Shell & Layout

```
App
└── AuthProvider (Zustand — token + currentUser)
    └── QueryClientProvider
        └── Router
            ├── /dang-nhap → LoginPage (standalone, no shell)
            └── /* → ProtectedLayout (AppLayout)
                 ├── TopBanner
                 │   ├── Logo/brand
                 │   ├── Notification bell (unread badge)
                 │   └── User avatar + dropdown (Đăng xuất)
                 ├── Sidebar (role-aware)
                 │   ├── Nav items filtered by role:
                 │   │   ├── AGENT: Trang chủ (/), Giỏ hàng chung (/gio-hang-chung)
                 │   │   ├── APPROVER: Trang chủ (/), Duyệt tin (/duyet/listing-post)
                 │   │   └── ADMIN: Trang chủ (/), Người dùng (/nguoi-dung), Tin nổi bật (/tin-noi-bat)
                 │   └── User menu: full name + Đăng xuất button
                 └── <Outlet /> (page content)
```

### Nav data model

```typescript
interface NavItem {
  label: string       // Vietnamese display text
  path: string
  roles: string[]     // Which roles can see this item
}
```

## 5. Route Guards

| Route Pattern | Guard | Behavior |
|--------------|-------|----------|
| `/dang-nhap` | `redirectIfAuth` | Redirect to `/` if token exists |
| `/` | `requireAuth` | Redirect to `/dang-nhap` if no token |
| `/tin/*` | `requireAuth` | Same |
| `/gio-hang-chung` | `requireAuth` | Same |
| `/thong-bao` | `requireAuth` | Same |
| `/duyet/*` | `requireAuth` + `requireRole(APPROVER, ADMIN)` | 403 page if AGENT |
| `/tin-noi-bat` | `requireAuth` + `requireRole(ADMIN)` | 403 page if not ADMIN |
| `/nguoi-dung*` | `requireAuth` + `requireRole(ADMIN)` | 403 page if not ADMIN |

403 page shows: "Bạn không có quyền truy cập trang này"

## 6. Auth Flow

```
LoginPage
  → useLoginState (state hook)
    → owns form via React Hook Form + Zod schema:
      schema = z.object({
        username: z.string().min(1, "Required"),
        password: z.string().min(8, "Min 8 characters"),
      })
    → form: UseFormReturn<ILoginForm>
  → LoginForm reads form from context, renders fields + errors
  → On submit: form.handleSubmit(handleLogin)
  → useLogin (action hook):
    → mutate({ username, password })
      → authRepository.login(username, password)
        → POST /api/v1/auth/login
    → onSuccess:
      → authStore.login(token, user)
      → queryClient.setQueryData(['auth', 'me'], user)
      → navigate('/')
    → onError:
      → if 401 → set form error "Sai tên đăng nhập hoặc mật khẩu"
      → if deactivated → set form error "Tài khoản đã bị vô hiệu hoá"
      → (action hook never rethrows — returns error state consumed by LoginForm)

Logout:
  → user clicks "Đăng xuất"
  → authStore.logout()
  → queryClient.clear()
  → navigate('/dang-nhap')

On app mount:
  authStore.hydrate()  // Read token from localStorage
  if (token) → authRepository.getMe()
    → 200: set currentUser
    → 401: authStore.logout() + redirect
```

## 7. State Management

| State Category | Tool | Location | Examples |
|---------------|------|----------|---------|
| Server state | TanStack Query `useQuery` | Facade state hooks | Listings, notifications, approvals, users |
| Server mutations | TanStack Query `useMutation` | Facade action hooks | Create/update/delete, approve/reject |
| Auth session | Zustand `authStore` | `stores/authStore.ts` | Token, currentUser, isAuthenticated |
| UI state | Zustand `uiStore` | `stores/uiStore.ts` | Sidebar expanded state, theme |
| Form state | React Hook Form `useForm` | Facade state hooks | Create/edit listing, login, user forms |
| Form schema | Zod `z.object()` | Facade state hooks | Validation rules co-located with form |

### Layer responsibilities

| Layer | Manages |
|-------|---------|
| Data (repository) | API calls, DTO transformation |
| Facade state hook | `useQuery` calls, form state, UI state, pagination state, filter state, mode flags |
| Facade action hook | `useMutation` calls, side effects (toast, navigate, invalidateQueries) |
| View | Reads from state hook, calls mutate on action hook, renders UI |

### Zustand stores

```typescript
// stores/authStore.ts
interface AuthState {
  token: string | null
  currentUser: ICurrentUser | null
  isAuthenticated: boolean
  login: (token: string, user: ICurrentUser) => void
  logout: () => void
  setUser: (user: ICurrentUser) => void
}

// stores/uiStore.ts
interface UIState {
  sidebarExpanded: boolean
  sidebarMobileOpen: boolean
  toggleSidebar: () => void
  setSidebarMobileOpen: (open: boolean) => void
}
```

## 8. Data Layer

### HTTP Client

```typescript
// data/infra/httpClient.ts
const httpClient = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — inject token
httpClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor — normalize errors, handle 401
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/dang-nhap'
    }
    return Promise.reject(normalizeError(error))
  },
)
```

### Repository pattern

```typescript
// data/repositories/listingRepository.ts
export const listingRepository = {
  list(params: ListingListParams): Promise<PaginatedResponse<ListingDTO>> {
    return httpClient.get('/listings', { params }).then(r => r.data)
  },
  get(id: string): Promise<ListingDetailDTO> {
    return httpClient.get(`/listings/${id}`).then(r => r.data)
  },
  create(data: CreateListingDTO): Promise<ListingDTO> {
    return httpClient.post('/listings', data).then(r => r.data)
  },
  update(id: string, data: UpdateListingDTO): Promise<ListingDTO> {
    return httpClient.put(`/listings/${id}`, data).then(r => r.data)
  },
  delete(id: string): Promise<void> {
    return httpClient.delete(`/listings/${id}`)
  },
  submit(id: string): Promise<ListingDTO> {
    return httpClient.post(`/listings/${id}/submit`).then(r => r.data)
  },
  withdraw(id: string): Promise<ListingDTO> {
    return httpClient.post(`/listings/${id}/withdraw`).then(r => r.data)
  },
}
```

### Query key factories

```typescript
// data/queries/listingQueries.ts
export const listingQueries = {
  all: ['listings'] as const,
  lists: () => [...listingQueries.all, 'list'] as const,
  list: (params: ListingListParams) => [...listingQueries.lists(), params] as const,
  details: () => [...listingQueries.all, 'detail'] as const,
  detail: (id: string) => [...listingQueries.details(), id] as const,
  hot: () => [...listingQueries.all, 'hot'] as const,
  myPins: () => [...listingQueries.all, 'myPins'] as const,
}
```

## 9. Form Pattern (React Hook Form + Zod)

### State hook owns the form

```typescript
// pages/listing-form/facades/useListingFormState.ts
const listingFormSchema = z.object({
  transactionType: z.enum(['BAN', 'CHO_THUE', 'SANG_NHUONG']),
  propertyType: z.string().min(1, 'Vui lòng chọn loại'),
  price: z.coerce.number({ required_error: 'Vui lòng nhập giá' }).positive(),
  commissionType: z.enum(['PERCENTAGE', 'FLAT']),
  commissionValue: z.coerce.number({ required_error: 'Vui lòng nhập hoa hồng' }).positive(),
  areaWidth: z.coerce.number({ required_error: 'Vui lòng nhập chiều rộng' }).positive(),
  areaLength: z.coerce.number({ required_error: 'Vui lòng nhập chiều dài' }).positive(),
  totalArea: z.coerce.number({ required_error: 'Vui lòng nhập diện tích' }).positive(),
  numRooms: z.coerce.number().min(0),
  numBathrooms: z.coerce.number().min(0),
  numFloors: z.coerce.number().min(0),
  streetName: z.string().min(1, 'Vui lòng nhập tên đường'),
  houseNumber: z.string().min(1, 'Vui lòng nhập số nhà'),
  ward: z.string().min(1, 'Vui lòng chọn phường/xã'),
  district: z.string().min(1, 'Vui lòng chọn quận/huyện'),
  city: z.string().min(1, 'Vui lòng chọn thành phố'),
  ownerPhone: z.string().min(1, 'Vui lòng nhập số điện thoại'),
  description: z.string().min(1, 'Vui lòng nhập mô tả'),
  // Optional fields
  title: z.string().optional(),
  label: z.string().optional(),
  furnishing: z.string().optional(),
  frontageType: z.string().optional(),
  legalStatus: z.string().optional(),
  direction: z.string().optional(),
  roadWidth: z.string().optional(),
  videoUrl: z.string().url('Link không hợp lệ').optional().or(z.literal('')),
  action: z.enum(['save', 'submit']).optional(),
})

export type IListingForm = z.infer<typeof listingFormSchema>

export function useListingFormState(existingListing?: ListingDTO | null) {
  const [mode] = useState<'create' | 'edit'>(existingListing ? 'edit' : 'create')
  const defaultValues = existingListing ? listingToFormValues(existingListing) : undefined

  const form = useForm<IListingForm>({
    resolver: zodResolver(listingFormSchema) as unknown as Resolver<IListingForm>,
    defaultValues: defaultValues ?? {
      transactionType: 'BAN',
      city: 'Hồ Chí Minh',
      numRooms: 0,
      numBathrooms: 0,
      numFloors: 0,
      commissionType: 'PERCENTAGE',
    },
    mode: 'onSubmit',
  })

  const watchedTransactionType = form.watch('transactionType')

  return { form, mode, watchedTransactionType }
}
```

### Action hook receives validated data

```typescript
// pages/listing-form/facades/useCreateListing.ts
export function useCreateListing() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: async (data: IListingForm & { images: File[] }) => {
      const payload = formToCreatePayload(data)
      const listing = await listingRepository.create(payload)
      if (data.images.length > 0) {
        for (const file of data.images) {
          await listingRepository.uploadImage(listing.id, file)
        }
      }
      return listing
    },
    onSuccess: (listing) => {
      queryClient.invalidateQueries({ queryKey: listingQueries.lists() })
      toast.success('Tạo tin đăng thành công')
      navigate(`/tin/${listing.id}`)
    },
    onError: (error: ApiError) => {
      toast.error(error.message)
    },
  })
}
```

### View calls mutate with validated data

```tsx
// pages/listing-form/CreateListingPage.tsx
function CreateListingPage() {
  const { form, mode } = useListingFormState()
  const { mutate: create, isPending: isCreating } = useCreateListing()

  const onSubmit = form.handleSubmit((data) => {
    // data is fully validated by Zod — View just calls mutate
    create(data)
  })

  return (
    <FormProvider {...form}>
      <form onSubmit={onSubmit}>
        <PageHeader title="Nhập hàng mới" backPath="/" />
        <BasicInfoSection />
        <PropertyDetailsSection />
        <CommissionSection />
        <LocationSection />
        <ContactSection />
        <ImageUploader />
        <Button type="submit" disabled={isCreating}>
          {isCreating ? 'Đang tạo...' : 'Đăng tải'}
        </Button>
      </form>
    </FormProvider>
  )
}
```

## 10. Validation Flow

```
Zod schema (defined in state hook)
  → zodResolver wraps it for React Hook Form
  → form.handleSubmit validates on submit
  → field-level errors populate formState.errors
  → View reads errors via <Controller> or formState
  → handleSubmit only fires callback when data is valid
  → Action hook receives validated I<Name> data — no re-validation
```

### All forms with their Zod schemas

| Feature | State Hook | Schema |
|---------|-----------|--------|
| Login | `useLoginState` | `{ username: z.string(), password: z.string().min(8) }` |
| Create Listing | `useListingFormState` | `listingFormSchema` (full listing fields + images) |
| Edit Listing | `useListingFormState` | `listingFormSchema` (same, pre-filled via `listingToFormValues` mapper) |
| Report Deposit | `useProductDetailState` | `{ customerName: z.string().min(2), customerPhone: z.string(), depositAmount: z.number().positive() }` |
| Report Cancellation | `useProductDetailState` | `{ reason: z.string().min(1, 'Vui lòng nhập lý do') }` |
| Create User | `useUserFormState` | `{ fullName: z.string().min(1), username: z.string().min(3), password: z.string().min(8), role: z.enum([...]) }` |
| Edit User | `useUserFormState` | Same as create, password optional |
| Reject Approval | `useApprovalQueueState` | `{ reason: z.string().min(1, 'Vui lòng nhập lý do từ chối') }` |

## 11. Data Flow Examples

### Browse shared cart (read)

```
SharedCartPage (View)
  → useSharedCartState (Facade State hook)
    → useQuery({
        queryKey: listingQueries.list({ page, filter, search, transactionType }),
        queryFn: () => listingRepository.list(params),
      })
    → mapper.toUIList(dto) → IListingCard[]
    → state: { listings, totalCount, isLoading, filter, page }
  → Decomposes into:
    <HotProductStrip />     ← read from separate useQuery
    <FilterTabs />          ← read filter, call setFilter
    <SearchBar />           ← read search, call setSearch
    <ListingGrid>
      <ListingCard />       ← read IListingCard props
    </ListingGrid>
    <Pagination />           ← read page / totalPages, call setPage
```

### Report deposit (write)

```
ProductDetailPage (View)
  → reads listing from useProductDetailState
  → user clicks "Báo khách cọc"
    → useProductDetailState opens deposit form dialog
      → form is owned by state hook (RHF + Zod)
      → form fields: customerName, customerPhone, depositAmount
  → user fills form + submits
    → form.handleSubmit(onDepositSubmit)
  → onDepositSubmit receives validated IReportDeposit
    → useReportDeposit (Action hook)
      → mutate(data)
        → dealEventRepository.reportDeposit(listingId, payload)
          → POST /api/v1/listings/{id}/deal-events/deposit
        → onSuccess:
          → queryClient.invalidateQueries({ queryKey: listingQueries.detail(listingId) })
          → queryClient.invalidateQueries({ queryKey: notificationQueries.unreadCount() })
          → toast.success("Báo cọc thành công, chờ duyệt")
          → close dialog
        → onError (409):
          → toast.error("Bất động sản này đã được báo cọc trước đó")
```

## 12. Error Handling

```
DATA LAYER:
  httpClient interceptor normalizes all errors → ApiError
  Repository throws ApiError — TanStack Query catches it

FACADE ACTION HOOK (useMutation onError):
  → If 4xx business error: show toast with code-specific message
    → "ALREADY_PROCESSED" → "Yêu cầu đã được xử lý"
    → "DUPLICATE_DEPOSIT" → "Bất động sản đã được báo cọc"
    → "INVALID_STATUS_TRANSITION" → "Trạng thái không hợp lệ"
    → "LAST_ADMIN" → "Không thể thay đổi ADMIN cuối cùng"
    → "MAX_HOT_ITEMS" → "Đã đạt số lượng HOT tối đa (14)"
    → "USERNAME_TAKEN" → "Tên đăng nhập đã tồn tại"
  → If 5xx: show generic toast "Có lỗi xảy ra, vui lòng thử lại"
  → Never rethrows to View

FACADE STATE HOOK (useQuery error):
  → Error state returned: { isLoading, isError, error, refetch }
  → View renders <ErrorState message={...} onRetry={refetch} />

VIEW:
  → Loading: <LoadingSpinner />
  → Error: <ErrorState message={error.message} onRetry={refetch} />
  → Empty: <EmptyState message="Không có dữ liệu" actionLabel="..." />
  → Success: render data
```

## 13. Facade Coordination Rules

### State hooks (useXxxState)
- Own `useState` for UI state: mode, filters, pagination, selected items
- Own `useForm` for form state when applicable
- Own `useQuery` for server data
- Read auth/user from `useAuthContext()` or `authStore`
- NEVER import action hooks
- NEVER call `navigate`, `toast()`, or other side effects
- NEVER call `mutate` or `queryClient.invalidateQueries`
- Return: `{ form?, mode?, data?, isLoading, isError, error, filters, setFilter, page, setPage, ... }`

### Action hooks (useXxxAction)
- Use `useMutation` exclusively
- `mutationFn`: validate → mapper.toPayload() → repository.mutate()
- `onSuccess`: queryClient.invalidateQueries() → navigate() / toast()
- `onError`: toast() with user-facing message
- NEVER import state hooks
- NEVER accept error callbacks from View
- NEVER rethrow errors to View
- Return: `{ mutate, isPending, variables, ... }`

### View (Page components)
- Call state hook → destructure `form`, data, loading, error, actions
- Call action hook → destructure `mutate`, `isPending`
- Read state from state hook only; pass to child components
- Call `mutate(data)` unconditionally — no guards, no branching
- Call `form.handleSubmit(onSubmit)` — no inline validation logic
- NEVER use `useState` / `useReducer` / `useRef`
- NEVER import DTO types, repositories, or httpClient
- NEVER call `navigate` or `toast()` after mutate

## 14. Shared Components

### Layout components

| Component | Purpose |
|-----------|---------|
| `AppLayout` | TopBanner + Sidebar + Outlet |
| `Sidebar` | Role-aware nav with accordion menus, pending count badges |
| `SidebarNavItem` | Single nav link with optional badge |
| `TopBanner` | Notification bell with unread badge, user avatar dropdown |

### shadcn component map

These components come from shadcn/ui (installed via CLI). They live in `shared/components/ui/` and follow the Radix accessibility + Tailwind patterns. Use them directly — no custom wrappers.

| shadcn Component | Replaces | Notes |
|------------------|----------|-------|
| `button` | — | Base button with variants; wrap in `LoadingButton` pattern for isPending state |
| `card` | — | Card shell; compose with `CardHeader`, `CardContent`, `CardFooter` |
| `badge` | — | Status badges, HOT tags, commission labels |
| `dialog` | `ConfirmDialog` | Modal with `DialogTrigger`, `DialogContent`, `DialogFooter` |
| `dropdown-menu` | — | User avatar dropdown in `TopBanner` |
| `input`, `select`, `textarea`, `label`, `form` | — | Form field components; use with React Hook Form `<Controller>` |
| `table` | — | User list table |
| `pagination` | — | Page navigation |
| `tabs` | — | Filter tabs on SharedCart, Notifications, MyCart |
| `accordion` | — | Queue menu accordion groups in Sidebar |
| `sheet` | — | Mobile sidebar drawer |
| `avatar` | — | User avatar in TopBanner |
| `skeleton` | — | Loading placeholders |
| `separator` | — | Divider lines |
| `popover` | — | Tooltip / popover info on listing cards |
| `sonner` | `ToastContext` | Toast notification system; add `<Toaster />` in `App.tsx`, call `toast()` directly |

### Custom app components (stay hand-rolled)

These are not provided by shadcn and remain custom in `shared/components/app/`:

| Component | Purpose |
|-----------|---------|
| `EmptyState` | Empty data placeholder with optional action |
| `ErrorState` | Error display with retry button |
| `LoadingSpinner` | Loading indicator |
| `ConfirmDialog` | Confirmation modal (uses shadcn `dialog` internally) |
| `SearchInput` | Debounced search input |

### Context providers

| Provider | Purpose | Exports |
|----------|---------|---------|
| `AuthContext` | Auth state, role checks | `useAuthContext()` → `{ user, role, isAuthenticated }` |

## 15. shadcn/ui Setup

### Installation

```bash
# Initialize shadcn with New York style and neutral base color
npx shadcn@latest init --style new-york --base-color neutral

# Add all required components
npx shadcn@latest add button card badge dialog dropdown-menu \
  input select textarea label form \
  table pagination \
  tabs accordion \
  sheet popover \
  avatar skeleton separator scroll-area sonner
```

### Integration with existing config

| Config | Value | Notes |
|--------|-------|-------|
| `style` | `new-york` | Compact design, smaller paddings, subtle borders |
| `baseColor` | `neutral` | Clean gray palette, pairs with any accent |
| `cssVariables` | `true` | Enables CSS variable theming |
| `components` | `shared/components/ui` | Matches feature-based structure — NOT the default `components/ui` |
| `utils` | `shared/lib/utils` | `cn()` utility re-exported for all shadcn components |

### TailwindCSS configuration

The shadcn init adds Tailwind config for CSS variables (colors, borders, rings). This integrates with the existing Tailwind setup — no conflict with custom class names.

### Post-installation

After running the CLI commands:
- `shared/components/ui/` is populated with all component files
- `shared/lib/utils.ts` is generated with the `cn()` utility
- `tailwind.config.ts` is updated with CSS variable references
- `app/globals.css` contents are merged into `index.css`

> shadcn components are meant to be edited. Tweak colors, sizes, and variants in the generated `.tsx` files as needed for the Biglands design language.

## 16. Naming Conventions

| Pattern | Convention | Example |
|---------|-----------|---------|
| UI Types | `I<Name>` | `IListing`, `IUser`, `INotification` |
| DTO Types | `<Name>DTO` (in `<name>.dto.ts`) | `ListingDTO`, `UserDTO` |
| State Hook | `use<Feature>State` | `useSharedCartState`, `useLoginState` |
| Action Hook | `use<Action><Feature>` | `useReportDeposit`, `useCreateListing` |
| Page Component | `<Name>Page` | `SharedCartPage`, `CreateListingPage`, `EditListingPage` |
| Repository | `<name>Repository` | `listingRepository`, `userRepository` |
| Query Keys | `<name>Queries` | `listingQueries`, `notificationQueries` |
| Constants | `<name>UI` | `listingUI`, `queueUI` |
| Shared Component | PascalCase | `Sidebar`, `ConfirmDialog`, `Badge` |

## 17. Key Invariants

1. **Layer isolation**: View never imports from `data/`. Facade never imports View. Data never imports Facade or View types.
2. **State hooks own forms**: No form logic in View components. All `useForm` calls in facades only.
3. **Action hooks own side effects**: `navigate`, `toast()`, `invalidateQueries` only in action hook `onSuccess`/`onError`. View never calls these after `mutate`.
4. **View calls `mutate(data)` unconditionally**: All guards, branching, and validation live in facades.
5. **No `useState` in page components**: Component state belongs in state hooks.
6. **No DTO types in View**: Mapper hooks transform DTO → I types at the facade boundary.
7. **One action hook per mutation**: No combined auth actions (`useAuthActions` with login + logout).
8. **Query invalidation on mutation success**: Actions invalidate related queries. State hooks refetch automatically.
9. **Error normalization at API boundary**: All errors become `ApiError` with code, message, details.
10. **Product code generation**: Server-side only — frontend receives generated code in response, never generates locally.

## 18. Feature-to-API Mapping

| Feature | API Endpoints Used | Repositories |
|---------|-------------------|--------------|
| Auth | `POST /auth/login`, `POST /auth/logout`, `GET /auth/me` | `authRepository` |
| Shared Cart | `GET /listings`, `GET /hot-listings`, `PUT /listings/{id}/pin`, `DELETE /listings/{id}/pin`, `GET /users/me/pins` | `listingRepository`, `pinRepository`, `hotProductRepository` |
| Product Detail | `GET /listings/{id}`, `POST /listings/{id}/deal-events/deposit`, `POST /listings/{id}/deal-events/closure`, `POST /listings/{id}/deal-events/cancellation`, `POST /listings/{id}/deal-events/sold-out` | `listingRepository`, `dealEventRepository` |
| My Cart | `GET /listings?createdBy=me`, `DELETE /listings/{id}`, `POST /listings/{id}/withdraw` | `listingRepository` |
| Create/Edit Listing | `POST /listings`, `PUT /listings/{id}`, `POST /listings/{id}/submit`, `POST /listings/{id}/images`, `PUT /listings/{id}/images/reorder`, `DELETE /listings/{id}/images/{imageId}`, `PUT /listings/{id}/images/{imageId}/primary` | `listingRepository`, `listingImageRepository` |
| Notifications | `GET /notifications`, `GET /notifications/unread-count`, `PATCH /notifications/{id}/read`, `POST /notifications/read-all` | `notificationRepository` |
| Approval Queues | `GET /approvals/queues`, `GET /approvals/queues/{queueType}`, `POST /approvals/{id}/approve`, `POST /approvals/{id}/reject`, `POST /approvals/bulk-approve` | `approvalRepository` |
| User Management | `GET /users`, `GET /users/{id}`, `POST /users`, `PUT /users/{id}`, `PATCH /users/{id}/deactivate`, `PATCH /users/{id}/reactivate`, `PATCH /users/{id}/role` | `userRepository` |
| Hot Products | `GET /hot-listings`, `POST /listings/{id}/promote`, `DELETE /listings/{id}/promote`, `PUT /hot-listings/reorder` | `hotProductRepository` |
| Geography | `GET /geography/cities`, `GET /geography/cities/{cityId}/districts`, `GET /geography/cities/{cityId}/districts/{districtId}/wards` | `geographyRepository` |

---

*End of Frontend Architecture — Biglands v1.0*
