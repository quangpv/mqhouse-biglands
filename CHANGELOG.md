# Changelog

## 1.0.0 (2026-06-22)

### Phase 1 — Foundation
- Vite + React + TypeScript project setup
- shadcn/ui (New York, neutral) component library integration
- AppLayout, AuthGuard, RoleGuard shared components
- HTTP client with 401 intercept and QueryClient provider
- Zustand auth store with token persistence

### Phase 2 — Auth UI
- Login page with React Hook Form + Zod validation
- 401 intercept → automatic redirect to login
- Auth guard with role-based access control

### Phase 3 — Shared Cart (Homepage)
- ListingCard with skeleton loading state
- Hot products horizontal strip
- Paginated listing grid with filter tabs (all/hot/pinned)
- Pin/unpin functionality, search, "Nhập hàng mới" button

### Phase 4 — Product Detail
- ListingGallery, KeyInfoSection, DealActionButtons
- Deposit, closure, cancellation, sold-out deal actions
- ReviewsSection with create/delete/image-upload
- AgentContactInfo

### Phase 5 — Listing Form
- BasicInfoSection, PropertyDetailsSection
- LocationSection with LocationCascade (city/district/ward)
- CommissionSection, ContactSection, ImageUploader
- Create and Edit listing pages

### Phase 6 — Cart, Notifications, Reviews
- MyCartPage with status filter tabs
- NotificationsPage with preferences sheet + mark-read
- Review data layer (DTO, repository, queries) + UI components
- Home page polish (hot strip, pagination, create button)

### Phase 7 — Admin Modules
- **Approval Queue** (SC-008): queue pages, 4 facades, 5 components
- **User Management** (SC-009/010): list/create/edit pages, user table/form/dialogs
- **Hot Products** (SC-011): hot products page, reorder/promote/remove

### Backend (13 modules)
- auth, users, listings, listing_images, deal_events, approvals
- notifications, hot_products, pins, user_settings, geography
- reviews, organizations
- Forgot password + reset password endpoints
