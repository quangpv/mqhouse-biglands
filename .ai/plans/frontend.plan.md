# Frontend Implementation Plan — Biglands

> B2B real estate marketplace for CHDV (serviced apartments) in HCMC.
> Roles: AGENT, APPROVER, ADMIN. Vietnamese UI.

## Foundation (must be done first)

| Item | Details |
|---|---|
| Init project | Vite + React + TypeScript, shadcn/ui New York neutral |
| Theme | CSS variables, dark mode toggle |
| Shared UI | shadcn: button, input, card, dialog, toast, badge, avatar, table, pagination, tabs, dropdown, skeleton, progress, label, separator, alert, sheet |
| App components | `AppLayout` (header + sidebar), `MainLayout`, `AuthGuard`, `RoleGuard`, `PageHeader`, `DataTable`, `ConfirmDialog`, `FormField`, `EmptyState`, `LoadingScreen`, `ErrorDisplay` |
| HTTP client | Axios instance, interceptors (token attach, 401 → logout, error transform) |
| React Query | `queryClient` defaults (stale 30s, retry 1), `ApiError` type |
| Auth store | Zustand: `token`, `user`, `setAuth`, `clearAuth`, `isAuthenticated`, `hasRole` |
| Error type | `ValidationError` for form-level errors |
| Utils | `cn()`, `formatPrice()`, `formatDate()`, `formatArea()`, `formatPhone()`, `getStatusColor()`, `getTransactionTypeLabel()`, `getPropertyTypeLabel()` |
| Route map | `src/routes/` — see routing section below |

## Module 1: Auth UI

| Item | Details |
|---|---|
| Screens | Login (`/dang-nhap`) |
| APIs | `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |
| State | `useAuthState` (form: email, password, remember) |
| Actions | `useLoginAction` |
| Components | `LoginForm`, `LoginCard` |
| Validation | Zod — email (email format), password (min 6) |
| States | loading (Spinner), error (toast + field error), success (redirect) |
| Edge cases | expired token → clear + show login; "Quên mật khẩu?" link (no backend — defer) |

## Module 2: Shared Cart Browse (Homepage)

| Item | Details |
|---|---|
| Screens | Homepage (`/`) |
| APIs | `GET /api/v1/listings` (query: transactionType, propertyType, district, priceMin, priceMax, keyword, sortBy, sortDir, page, size) |
| State | `useBrowseListingsState` (filters form, pagination) |
| Actions | `useBrowseListingsAction` |
| Components | `ListingCard`, `ListingGrid`, `SearchBar`, `FilterPanel`, `Pagination` |
| Feature | Pin/unpin `POST/DELETE /api/v1/listings/{id}/pin` |
| States | loading (card skeletons), empty ("Chưa có tin đăng"), error (retry), filtered-empty ("Không tìm thấy kết quả") |
| Note | `totalCount` = CON_HANG only (BR-015) |

## Module 3: Product Detail

| Item | Details |
|---|---|
| Screens | Listing Detail (`/tin/{id}`), own-draft read-only view |
| APIs | `GET /api/v1/listings/{id}` (returns `creator`, `pricePerM2`, `requiresApproval`), `GET /api/v1/listings/{id}/images` |
| State | `useListingDetailState` (listingId param) |
| Actions | `usePinAction`, `useDepositAction`, `useClosureAction`, `useCancellationAction`, `useSoldOutAction` |
| Components | `ListingGallery`, `ListingInfo`, `DealTimeline`, `DepositForm`, `ClosureForm`, `CancellationForm`, `SoldOutForm`, `ActionPanel` |
| Validation | deposit (customerName ≥2, depositAmount >0); cancellation (notes required) |
| States | loading (skeleton), not found (404), error (retry) |
| Edge cases | sold-out hides deal actions; own draft read-only; confirm dialogs before mutation; ownerPhone visible only to creator/admin/approver |

## Module 4: Listing Form (Create / Edit)

| Item | Details |
|---|---|
| Screens | Create (`/dang-tin`), Edit (`/chinh-sua-tin/{id}`) |
| APIs | `POST /api/v1/listings` (action: save|submit), `PUT /api/v1/listings/{id}`, image upload/reorder/delete |
| State | `useListingFormState` (3-step wizard: Info → Location → Media) |
| Actions | `useCreateListingAction`, `useUpdateListingAction`, `useUploadImagesAction`, `useDeleteImageAction`, `useReorderImagesAction` |
| Components | `ListingFormWizard`, `BasicInfoStep`, `LocationStep`, `MediaStep`, `ImageDropzone`, `ImagePreview`, `FormNavigation` |
| Validation | Full Zod schema matching CreateListingRequest (see OpenAPI) |
| States | loading (skeleton for edit), submitting (progress), error (field errors), success toast, redirect |
| Edge cases | edit CON_HANG → re-approval (LST-I05); DRAFT always editable; exit confirmation dirty; save vs submit; transactionType locked when status=DA_COC |

## Module 5: My Cart

| Item | Details |
|---|---|
| Screens | My Cart (`/gio-hang-chung`), My Cart Detail (`/gio-hang-chung/{id}`) |
| APIs | `GET /api/v1/listings?createdBy={me}` (supports `status=CON_HANG,DA_COC` multi-value via `createdBy`), `GET /api/v1/listings/{id}` |
| State | `useMyListingsState` (tabs: CON_HANG, PENDING_APPROVAL, DRAFT, SOLD, CANCELLED) |
| Actions | `useDeleteListingAction`, `useRecallAction` |
| Components | `MyListingCard`, `MyListingTabs`, `ListingActionMenu` |
| States | tab-empty per status message |
| Risk | `createdBy` filter may need backend confirmation (OQ-01) |

## Module 6: Notifications

| Item | Details |
|---|---|
| Screens | Notifications (`/thong-bao`) |
| APIs | `GET /api/v1/notifications?transactionType=&q=` (returns `unreadCount`, `categoryCounts`; items include `eventType`, `actorName`, `transactionType`), `PATCH .../read`, `PATCH .../read-all`, `GET .../unread-count`, `GET|PUT .../notification-preferences` |
| State | `useNotificationListState` (pagination) |
| Actions | `useMarkReadAction`, `useMarkAllReadAction`, `useUpdatePreferencesAction` |
| Components | `NotificationList`, `NotificationItem`, `NotificationBadge`, `NotificationPreferencesPanel` |
| States | empty ("Không có thông báo nào"), loading (skeleton list) |
| Edge cases | click → mark read + navigate; periodic unread polling |

## Module 7: Approval Queue

| Item | Details |
|---|---|
| Screens | Queue list (`/duyet/{queueType}`), Queue Detail (`/duyet/{queueType}/{id}`) |
| APIs | `GET /api/v1/approval/queues`, `GET .../queues/{type}?dateFrom=&dateTo=&agentId=` (items include `dealEvent` with customer info, `reportedBy`), `GET .../items/{id}`, `POST .../items/{id}/approve`, `POST .../items/{id}/reject`, `POST /api/v1/approval/bulk-approve` |
| State | `useApprovalQueueState` (queueType, transactionType, pagination) |
| Actions | `useApproveAction`, `useRejectAction`, `useBulkApproveAction`, `useConfirmDealEventAction` |
| Components | `QueueList`, `QueueItemCard`, `ApproveRejectPanel`, `RejectDialog`, `BulkApproveBar` |
| Validation | reject reason (min 1 char) |
| States | queue empty (per type), no queues empty |
| Edge cases | bulk partial failure; re-approval for price change; CON_HANG→SOLD auto-approve |

## Module 8: User Management

| Item | Details |
|---|---|
| Screens | User List (`/nguoi-dung`), Create (`.../tao-moi`), Edit (`.../{id}`) |
| APIs | `GET /api/v1/users`, `POST /api/v1/users` (password optional → auto-generated; response includes `generatedPassword`), `PUT /api/v1/users/{id}`, `PATCH .../deactivate`, `.../activate`, `.../role` |
| State | `useUserListState` (pagination, role filter), `useUserFormState` |
| Actions | `useCreateUserAction`, `useUpdateUserAction`, `useToggleActiveAction`, `useChangeRoleAction` |
| Components | `UserTable`, `UserForm`, `UserStatusBadge`, `RoleSelect`, `DeactivateConfirmDialog` |
| Validation | email (email), fullName (2-100), phone (pattern), password (min 8 — create only) |
| States | empty ("Chưa có người dùng nào") |
| Edge cases | self-deactivation prevention; self-role-change prevention |

## Module 9: Hot Products

| Item | Details |
|---|---|
| Screens | Hot Products Management (`/tin-noi-bat`) |
| APIs | `GET /api/v1/listings?isHot=true` (also supports `isHot=false` to find non-hot listings to promote), `POST .../promote`, `DELETE .../hot`, `PUT /api/v1/hot/reorder` |
| State | `useHotListingsState` |
| Actions | `usePromoteAction`, `useRemoveHotAction`, `useReorderHotAction` |
| Components | `HotList`, `HotListItem`, `ReorderPanel`, `PromoteDialog` |
| Validation | hotOrder (1-14, unique) |
| States | empty ("Chưa có tin nổi bật nào") |
| Edge cases | max 14 (LST-C08); reorder shifts remaining items |

## Routing Plan

```
/dang-nhap                    → Auth UI         (no auth)
/                             → Shared Cart     (auth optional)
/tin/{id}                     → Product Detail   (auth optional browse, auth for actions)
/dang-tin                     → Listing Form     (AGENT+)
/chinh-sua-tin/{id}           → Listing Form     (AGENT+)
/gio-hang-chung               → My Cart          (AGENT+)
/gio-hang-chung/{id}          → My Cart Detail   (AGENT+)
/thong-bao                    → Notifications    (auth)
/duyet/{queueType}            → Approval Queue   (APPROVER+)
/duyet/{queueType}/{id}       → Approval Detail  (APPROVER+)
/nguoi-dung                   → User List        (ADMIN)
/nguoi-dung/tao-moi           → Create User      (ADMIN)
/nguoi-dung/{id}              → Edit User        (ADMIN)
/tin-noi-bat                  → Hot Products     (ADMIN)
*                             → 403 / 404
```

## Graph Dependencies

```
Foundation ─┬─ Auth ── Shared Cart ── Product Detail ── Listing Form
            │                                              │
            └──────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
               My Cart          Approval Queue
                    │                   │
                    ▼                   ▼
            Notifications        User Management
                                       │
                                       ▼
                                 Hot Products
```

## Implementation Order

1. **Foundation** — project setup, shadcn, shared components, data layer, route shell
2. **Auth UI** — login, every module needs auth
3. **Shared Cart Browse** — homepage, visible to all roles immediately
4. **Product Detail** — linked from cards, enables deal/deposit flows
5. **Listing Form** — borrows detail patterns for prefilled edit
6. **My Cart** — reuses browse + detail patterns
7. **Notifications** — standalone, referenced from detail
8. **Approval Queue** — parallel to Notifications
9. **User Management** — relies on approval patterns for role
10. **Hot Products** — depends on listing admin patterns (last)

