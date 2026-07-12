# Types

All enums, base types, core entities, request types, and response types.

## Enums

```
CommissionType = [PERCENTAGE, FLAT]
DirectionType = [EAST, WEST, SOUTH, NORTH, NORTHEAST, SOUTHEAST, NORTHWEST, SOUTHWEST]
Status = [draft, post_pending, edit_pending, deposit_pending, soldout_pending,
          complete_pending, cancel_pending, reopen_pending, available,
          deposited, soldout, expired, completed]
Action = [submit, withdraw, deposit, soldout, cancel, complete, edit,
          approve, reject, expire, reopen]
NotificationType = [listing_post_created, listing_post_approved, listing_post_rejected,
                    editing_post_approved, edit_rejected,
                    deposit_reported, deposit_confirmed, deposit_rejected,
                    soldout_reported, soldout_confirmed, soldout_rejected,
                    cancellation_reported, cancellation_confirmed, cancellation_rejected,
                    closure_reported, closure_confirmed, closure_rejected,
                    listing_updated, listing_expired,
                    reopen_requested, reopen_approved, reopen_rejected]
ApprovalStatus = [pending, approved, rejected]
UserRole = [SALE, APPROVER, ADMIN]
EntityType = [review, property, avatar, certificate]
```

## Base Types

```
NumberRange = { from: number, to: number }
Geography = { name: string, id: string }
Province = Geography
Ward = Geography
District = Geography
PageDTO = { page: number, size: number, total_pages: number, total_items: number }
ListDTO<T> = { data: T[], metadata: PageDTO }
```

## Core Entity Types

### CreatorInfo
```
{
  id: UUID
  full_name: string
  phone: string | null
}
```

### FileInfo
```
{
  id: UUID
  origin_name: string
  path: string
  mimetype: string
  created_by: UUID
  entity_type: EntityType
  size: number
  thumbnail_320_url: string | null
  thumbnail_640_url: string | null
  created_at: Date
  updated_at: Date
}
```

### Property
```
{
  id: UUID
  code: string                          // 14-char: YYMMDD + 7-digit random
  transaction_type: string
  property_type: string
  title: string | null
  description: string
  price: number
  commission_type: CommissionType
  commission_value: number
  area_width: number
  area_length: number
  total_area: number
  num_rooms: number
  num_bathrooms: number
  num_floors: number
  street_name: string
  house_number: string
  address: string
  ward: string
  district: string
  city: string
  latitude: number | null
  longitude: number | null
  label: string | null
  furnishing: string | null
  frontage_type: string | null
  legal_status: string | null
  direction: DirectionType | null
  road_width: string | null
  owner_phone: string | null
  video_url: string | null
  status: Status
  is_hot: boolean | null
  hot_order: number | null
  view_count: number | null
  price_per_m2: number | null          // computed: price / total_area (2 decimals)
  primary_image_url: string | null
  images: FileInfo[]
  tags: TagInfo[]
  created_by_id: UUID
  creator: CreatorInfo | null
  approved_by_id: UUID | null
  approved_at: Date | null
  is_pinned: boolean
  requires_approval: boolean            // true for any *_pending status
  created_at: Date
  updated_at: Date
}
```

### PropertyTransition
```
{
  id: UUID
  property_id: UUID
  from_status: Status | null
  to_status: Status
  action: Action
  actor_id: UUID
  actor_name: string
  approval: Approval | null
  notes: string | null
  customer_name: string | null
  customer_phone: string | null
  contract_date: Date | null
  changed_fields: { [key: string]: { old: any, new: any } } | null
  file_ids: UUID[]
  created_at: Date
}
```

### Approval
```
{
  id: UUID
  transaction_type: string
  status: ApprovalStatus
  from_property_status: Status          // status before the request
  to_property_status: Status            // status after approval
  decided_by_id: UUID | null
  reason: string | null
  changed_fields: { [key: string]: { old: any, new: any } } | null
  decision_transition_id: UUID | null
  created_at: Date
}
```

### Review
```
{
  id: UUID
  property_id: UUID
  author_id: UUID
  author_name: string
  content: string
  images: FileInfo[]
  created_at: Date
  updated_at: Date
}
```

### User
```
{
  id: UUID
  full_name: string
  username: string
  phone: string | null
  email: string | null
  role: UserRole
  is_active: boolean
  avatar_url: string | null
  avatar_file_id: UUID | null
  device_limit_enabled: boolean
  organization_id: UUID | null
  organization_name: string | null
  property_type_ids: UUID[]
  transaction_type_ids: UUID[]
  created_at: Date
  updated_at: Date
}
```

### Organization
```
{
  id: UUID
  name: string
  display_name: string
  transaction_types: string[]
  property_types: string[]
  created_at: Date
}
```

### TagInfo
```
{
  id: string                           // primary key, auto-generated slug
  display_name: string
  created_at: Date
  updated_at: Date
}
```

### TransactionTypeInfo
```
{
  id: string
  code: string
  display_name: string
  created_at: Date
  updated_at: Date
}
```

### PropertyTypeInfo
```
{
  id: string
  code: string
  display_name: string
  created_at: Date
  updated_at: Date
}
```

### Notification
```
{
  id: UUID
  user_id: UUID
  title: string
  body: string
  reference_type: 'property' | 'approval' | 'deal_event' | null
  reference_id: UUID | null
  is_read: boolean
  event_type: string | null
  actor_name: string | null
  transaction_type: string | null
  created_at: Date
}
```

### NotificationPreferences
```
{
  email_notifications: boolean
  push_notifications: boolean
  sms_notifications: boolean
  digest_frequency: 'daily' | 'weekly' | 'none'
}
```

### HotProperty
```
{
  id: UUID
  property: Property
  start_time: Date
  end_time: Date
  created_by: UUID
  created_at: Date
}
```

---

## Request Types

### Auth
```
LoginRequest = { username: string, password: string }
RefreshTokenRequest = { refresh_token: string }
ForgotPasswordRequest = { email: string }
ResetPasswordRequest = { token: string, new_password: string }
ChangePasswordRequest = { current_password: string, new_password: string }
```

### Properties
```
PropertyInfo = {
  transaction_type_id: string
  property_type_id: string
  title: string | null
  description: string
  price: number
  commission_type: CommissionType
  commission_value: number
  area_width: number
  area_length: number
  total_area: number
  num_rooms: number                  // default 0
  num_bathrooms: number              // default 0
  num_floors: number                 // default 0
  street_name: string
  house_number: string
  address: string
  ward_id: string
  district_id: string
  province_id: string
  latitude: number | null
  longitude: number | null
  label: string | null
  furnishing: string | null
  frontage_type: string | null
  legal_status: string | null
  direction: DirectionType | null
  road_width: string | null
  owner_phone: string | null
  video_url: string | null
  image_ids: UUID[]                  // default []
  certificate_ids: UUID[]            // default []
  tag_ids: string[]                  // default []
}

CreatePropertyRequest = PropertyInfo & { is_draft: boolean }  // default true

UpdatePropertyRequest = Partial<PropertyInfo> & {
  tag_ids: string[] | null           // null = unchanged, [] = clear, [...] = replace
}

PropertyListParams = {
  search: string | null
  transaction_type_ids: string[] | null
  property_type_ids: string[] | null
  province_ids: string[] | null
  district_ids: string[] | null
  ward_ids: string[] | null
  direction_types: string[] | null
  room_count_from: int | null
  room_count_to: int | null
  area_from: float | null
  area_to: float | null
  width_from: float | null
  width_to: float | null
  price_from: float | null
  price_to: float | null
  statuses: Status[] | null
  tags: string[] | null
  is_hot: boolean | null
  created_by_id: UUID | null
  sort_by: 'created_at' | 'price' | 'view_count' | null
  sort_order: 'asc' | 'desc' | null
  page: number                       // default 1, min 1
  size: number                       // default 20, min 1, max 100
}

NotesRequest = { notes: string | null }

DepositRequest = {
  notes: string | null
  customer_name: string              // required
  customer_phone: string             // required
  contract_date: Date                // required, must be >= today
  file_ids: UUID[]                   // default [], max 10
}

CompleteRequest = DepositRequest

PromoteToHotRequest = {
  start_time: Date
  end_time: Date
}
```

### Approvals
```
ApprovalListParams = {
  transaction_type_ids: UUID[] | null
  status: ApprovalStatus[] | null
  search: string | null
  property_type_ids: UUID[] | null
  district: string[] | null
  ward: string[] | null
  price_from: number | null
  price_to: number | null
  area_from: number | null
  area_to: number | null
  requested_by_id: UUID | null
  sort_by: 'created_at' | 'price' | 'area' | null
  sort_order: 'asc' | 'desc' | null
  page: number
  size: number
}

ApprovalDecisionRequest = { reason: string | null }
```

### Users
```
CreateUserRequest = {
  full_name: string                  // required, max 255
  username: string                   // required, max 100, unique
  phone: string | null               // max 20
  email: string | null               // max 255, unique if provided
  password: string                   // required, min 6
  role: UserRole                     // required, cannot be ADMIN
  avatar_file_id: UUID | null
  device_limit_enabled: boolean      // default false
  organization_id: UUID | null
  property_type_ids: UUID[]          // default []
  transaction_type_ids: UUID[]       // default []
}

UpdateUserRequest = {
  full_name: string | null
  phone: string | null
  email: string | null
  is_active: boolean | null
  organization_id: UUID | null
  role: UserRole | null
  avatar_file_id: UUID | null
  property_type_ids: UUID[] | null
  transaction_type_ids: UUID[] | null
  device_limit_enabled: boolean | null
  // username is NOT updatable
}

ChangeUserPasswordRequest = { new_password: string }  // min 6
```

### Organizations
```
CreateOrganizationRequest = {
  name: string                       // required, unique
  display_name: string               // required
  transaction_types: string[]        // required
  property_types: string[]           // required
}

UpdateOrganizationRequest = CreateOrganizationRequest  // full replace, all fields required
```

### Meta Data
```
CreateTagRequest = { id: string | null, display_name: string }
UpdateTagRequest = { display_name: string }

CreateTransactionTypeRequest = { id: string, display_name: string }
UpdateTransactionTypeRequest = { display_name: string }

CreatePropertyTypeRequest = { id: string, display_name: string }
UpdatePropertyTypeRequest = { display_name: string }
```

### Reviews
```
CreateReviewRequest = { content: string, file_ids: UUID[] }
```

### Notifications
```
NotificationListParams = {
  is_read: bool | null
  transaction_type: string | null
  search: string | null
  page: number
  size: number
}

UpdateNotificationPrefsRequest = Partial<NotificationPreferences>
```

---

## Response Types

### Common
```
MessageResponse = { message: string }
```

### Auth
```
LoginResponse = { access_token: string, refresh_token: string }
RefreshTokenResponse = LoginResponse
```

### Profile
```
ProfileResponse = User
```

### Properties
```
PropertyResponse = Property
PropertyListResponse = ListDTO<Property>
PropertyCountResponse = {
  all_count: number
  hot_count: number
  pinned_count: number
}
PropertyTransitionResponse = PropertyTransition
PropertyTransitionListResponse = ListDTO<PropertyTransitionResponse>
```

### Approvals
```
ApprovalRequestDetail = {
  action: string
  from_status: Status | null
  to_status: Status
  notes: string | null
  customer_name: string | null
  customer_phone: string | null
  contract_date: Date | null
  file_ids: UUID[]
  changed_fields: { [key: string]: { old: any, new: any } } | null
}

DecisionInfo = {
  decided_by: CreatorInfo
  reason: string | null
  decided_at: Date
}

ApprovalResponse = {
  id: UUID
  property: Property
  transaction_type: string
  status: ApprovalStatus
  requested_by: CreatorInfo
  request: ApprovalRequestDetail
  decision: DecisionInfo | null
  created_at: Date
}

ApprovalListResponse = ListDTO<ApprovalResponse>
ApprovalCountItem = { transaction_type_id: string, action: string, count: number }
```

### Files
```
FileUploadResponse = { file_ids: UUID[] }
FileInfoResponse = FileInfo
```

### Reviews
```
ReviewListResponse = ListDTO<Review>
ReviewDetailResponse = Review
```

### Hot Properties
```
HotPropertyListResponse = ListDTO<HotProperty>
HotPropertyResponse = HotProperty
```

### Users
```
UserListResponse = ListDTO<User>
UserResponse = User
```

### Organizations
```
OrganizationListResponse = [Organization]
OrganizationResponse = Organization
```

### Transaction Types
```
TransactionTypeResponse = TransactionTypeInfo
TransactionTypeListResponse = [TransactionTypeInfo]
```

### Property Types
```
PropertyTypeResponse = PropertyTypeInfo
PropertyTypeListResponse = [PropertyTypeInfo]
```

### Tags
```
TagResponse = TagInfo
TagListResponse = [TagInfo]
```

### Geography
```
CityListResponse = [Province]
DistrictListResponse = [District]
WardListResponse = [Ward]
```

### Notifications
```
NotificationListResponse = ListDTO<Notification>
NotificationResponse = Notification
NotificationCountResponse = { items: [{ transaction_type: string, count: number }], total: number }
ReadAllResponse = { message: string }
```

### Notification Preferences
```
NotificationPrefsResponse = NotificationPreferences
```

### Carts
```
CartCountResponse = { [category: string]: number }
```
