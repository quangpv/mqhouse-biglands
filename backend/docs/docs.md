## Type ref:

### Enums
CommissionType = [PERCENTAGE, FLAT]
DirectionType = [EAST, WEST, SOUTH, NORTH, NORTHEAST, SOUTHEAST, NORTHWEST, SOUTHWEST]
Tag = [newest, best_selling, hot]
Status = [draff, post_pending, edit_pending, deposit_pending, soldout_pending, complete_pending, available, deposited, soldout, expired, completed]
Action = [submit, withdraw, deposit, soldout, cancel, complete]
NotificationType = [request_edit, request_post, request_deposit, request_soldout, request_cancel, request_complete]
ApprovalStatus = [pending, resolved, rejected]
UserRole = [sale, approver, admin]
EntityType = [review , property , avatar]

### Base types
NumberRange = {from:number, to:number}
Geography = {name:string, id:string}
Province = Geography
Ward = Geography
District = Geography
PageDTO = {page:number, size:number, total_pages:number}
ListDTO<T> = {data:T[], metadata:PageDTO}

### Core entity types
CreatorInfo = {
	id: UUID
	full_name: string
	phone: string | null
}

FileInfo = {
	id: UUID
	origin_name: string
	path: string
	mimetype: string
	created_by: UUID
	entity_type: EntityType
	size: number
}

Property = {
	id: UUID
	code: string
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
	price_per_m2: number | null
	primary_image_url: string | null
	images: FileInfo[]
	created_by_id: UUID
	creator: CreatorInfo | null
	approved_by_id: UUID | null
	approved_at: Date | null
	is_pinned: boolean
	requires_approval: boolean
	created_at: Date
	updated_at: Date
}

Approval = {
	id: UUID
	transaction_type: string
	status: ApprovalStatus
	decided_by_id: UUID | null
	reason: string | null
	created_at: Date
}

Review = {
	id: UUID
	property_id: UUID
	author_id: UUID
	author_name: string
	content: string
	images: FileInfo[]
	created_at: Date
	updated_at: Date
}

User = {
	id: UUID
	full_name: string
	username: string
	phone: string | null
	email: string | null
	role: UserRole
	is_active: boolean
	organization_id: UUID | null
	organization: Organization | null
	notification_prefs: NotificationPreferences | null
	created_at: Date
}

OrganizationInfo {
    name: string
	display_name: string
    transaction_types:string[]
    property_types:string[]
}

Organization = {
	id: UUID
	created_at: Date
} & OrganizationInfo

TransactionTypeInfo = {
	id: UUID
	code: string
	display_name: string
	created_at: Date
	updated_at: Date
}

PropertyTypeInfo = {
	id: UUID
	code: string
	display_name: string
	created_at: Date
	updated_at: Date
}

Notification = {
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

NotificationPreferences = {
	email_notifications: boolean
	push_notifications: boolean
	sms_notifications: boolean
	digest_frequency: 'daily' | 'weekly' | 'none'
}

### Request types

PropertyFilterRequest = {
	search: string | null
	transaction_type: string[] | null
	property_type: string[] | null
	tag: Tag[] | null
	district: District[] | null
	ward: Ward[] | null
	direction: DirectionType[] | null
	room_count: NumberRange | null
	area: NumberRange | null
	width: NumberRange | null
	price_range: NumberRange | null
	status: Status[] | null
}

DepositRequest = {
	notes: string | null
	customer_name: string
	customer_phone: string
	contract_date: Date
	file_ids: UUID[]
}

CompleteRequest = DepositRequest

PropertyInfo = {
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
	city: string | null
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
}

LoginRequest = { username: string, password: string }
RefreshTokenRequest = { refresh_token: string }
ForgotPasswordRequest = { email: string }
ResetPasswordRequest = { token: string, password: string }
ChangePasswordRequest = { current_password: string, new_password: string }

CreatePropertyRequest = { type: 'draff' | 'post_pending', data: PropertyInfo }
PropertyListParams = { is_hot: bool | null, is_pin: bool | null, created_by: 'me' | UUID | null, sort_by: 'created_at' | 'price' | 'view_count' | null, sort_order: 'asc' | 'desc' | null } & PropertyFilterRequest
UpdatePropertyRequest = { [key in PropertyInfo]: value }  // partial property fields

NotesRequest = { notes: string | null }

CreateReviewRequest = { content: string, file_ids: UUID[] }
PromoteToHotRequest = { start_time: Date, end_time: Date }

ApprovalListParams = { transaction_types: string[] | null, status: ApprovalStatus[] | null } & PropertyFilterRequest
ApproveRequest = { notes: string | null }
RejectRequest = { notes: string | null }

NotificationListParams = { is_read: bool | null, page: number, size: number }
UpdateNotificationPrefsRequest = Partial<NotificationPreferences>

UserListParams = { role: UserRole | null, is_active: bool | null, search: string | null, organization_id: UUID | null, page: number, size: number }
CreateUserRequest = { full_name: string, username: string, phone: string | null, email: string | null, password: string, role: UserRole, organization_id: UUID | null }
UpdateUserRequest = { full_name: string | null, phone: string | null, email: string | null, is_active: bool | null, organization_id: UUID | null }
UpdateUserRoleRequest = { role: UserRole }

CreateOrganizationRequest = OrganizationInfo
UpdateOrganizationRequest = OrganizationInfo

CreateTransactionTypeRequest = { code: string, display_name: string }
UpdateTransactionTypeRequest = { code: string, display_name: string }

CreatePropertyTypeRequest = { code: string, display_name: string }
UpdatePropertyTypeRequest = { code: string, display_name: string }

### Response types

MessageResponse = { message: string }

#### Auth
LoginResponse = { access_token: string, refresh_token:string }
RefreshTokenResponse = LoginResponse
LogoutResponse = MessageResponse
ForgotPasswordResponse = MessageResponse
ResetPasswordResponse = MessageResponse
ChangePasswordResponse = MessageResponse
UserProfileResponse = User

#### Profile
ProfileResponse = User

#### My Assets
MyPropertyListResponse = ListDTO<Property>
MyPinListResponse = ListDTO<Property>

#### Properties
PropertyResponse = Property
PropertyListResponse = ListDTO<Property>
StatusLogEntry = { id: UUID, property_id: UUID, from_status: Status | null, to_status: Status, actor_id: UUID, actor_name: string, approval: Approval | null, notes: string | null, created_at: Date }
StatusLogResponse = [StatusLogEntry]

#### Pins
PinResponse = { message: string }

#### Approvals

ApprovalResponse = {
	id: UUID
	property: Property
	transaction_type: string
	status: ApprovalStatus
	requested_by: CreatorInfo
	approve_details: {
		notes: string | null
		customer_name: string | null
		customer_phone: string | null
		contract_date: Date | null
		file_ids: UUID[] | null
	} | null
	created_at: Date
}

ApprovalListResponse = ListDTO<ApprovalResponse>
ApprovalDetailResponse = ApprovalResponse
ApprovalCountsResponse = { [type: string]: number }

#### Files
FileUploadResponse = { file_ids: UUID[] }
FileInfoResponse = FileInfo

#### Reviews
ReviewListResponse = ListDTO<Review>
ReviewDetailResponse = Review

#### Hot Properties
HotProperty = {
	id: UUID
	property: Property
	start_time: Date
	end_time: Date
	created_by: UUID
	created_at: Date
}

HotPropertyListResponse = [HotProperty]
HotPropertyResponse = HotProperty

#### Users
UserListResponse = ListDTO<User>
UserResponse = User

#### Organizations
OrganizationListResponse = [Organization]
OrganizationResponse = Organization

#### Transaction Types
TransactionTypeResponse = TransactionTypeInfo
TransactionTypeListResponse = [TransactionTypeInfo]

#### Property Types
PropertyTypeResponse = PropertyTypeInfo
PropertyTypeListResponse = [PropertyTypeInfo]

#### Geography
CityListResponse = [Province]
DistrictListResponse = [District]
WardListResponse = [Ward]

#### Notifications
NotificationListResponse = ListDTO<Notification>
NotificationResponse = Notification
NotificationCountResponse = { count: number }
ReadAllResponse = { message: string }

#### Notification Preferences
NotificationPrefsResponse = NotificationPreferences

---

## Auth
Prefix: `/auth`

POST /auth/login
Desc: Login
Rules: Public
Request: LoginRequest
Response: LoginResponse

POST /auth/refresh
Desc: Refresh access token
Rules: Public (requires valid refresh_token)
Request: RefreshTokenRequest
Response: RefreshTokenResponse

POST /auth/logout
Desc: Logout (blacklist token)
Rules: Authenticated
Response: LogoutResponse

POST /auth/change-password
Desc: Change current user's password
Rules: Authenticated
Request: ChangePasswordRequest
Response: ChangePasswordResponse

POST /auth/forgot-password
Desc: Request password reset
Rules: Public
Request: ForgotPasswordRequest
Response: ForgotPasswordResponse

POST /auth/reset-password
Desc: Reset password with token
Rules: Public
Request: ResetPasswordRequest
Response: ResetPasswordResponse

---

## Geography
Prefix: `/geography`

GET /geography/cities
Desc: List available cities
Rules: Public
Response: CityListResponse

GET /geography/cities/{city_id}/districts
Desc: List districts in a city
Rules: Public
Response: DistrictListResponse

GET /geography/cities/{city_id}/districts/{district_id}/wards
Desc: List wards in a district
Rules: Public
Response: WardListResponse

---

## WebSocket
Path: `/ws`

Desc: Real-time notification channel
Rules: Authenticated (token query param)
Connection: ws://host/ws?token={jwt_token}

Server messages:
{
	type: 'notification_created'
	data: Notification
}

{
	type: 'connection_established'
	data: { message: string }
}

{
	type: 'error'
	data: { message: string }
}

## Files

POST /files
Desc: Upload files (multipart)
Rules: Any authenticated
Request: Multipart { files: Part[] }
Response: FileUploadResponse

GET /files/{id}
Desc: Get file metadata
Rules: Any authenticated
Response: FileInfoResponse

---

## Transaction Types
Prefix: `/transaction-types`

GET /transaction-types
Desc: List all transaction types
Rules: Authenticated
Response: TransactionTypeListResponse

POST /transaction-types
Desc: Create transaction type
Rules: ADMIN
Request: CreateTransactionTypeRequest
Response: TransactionTypeResponse

GET /transaction-types/{id}
Desc: Get transaction type by id
Rules: Authenticated
Response: TransactionTypeResponse

PUT /transaction-types/{id}
Desc: Update transaction type
Rules: ADMIN
Request: UpdateTransactionTypeRequest
Response: TransactionTypeResponse

DELETE /transaction-types/{id}
Desc: Delete transaction type
Rules: ADMIN
Response: 204 No Content

---

## Property Types
Prefix: `/property-types`

GET /property-types
Desc: List all property types
Rules: Authenticated
Response: PropertyTypeListResponse

POST /property-types
Desc: Create property type
Rules: ADMIN
Request: CreatePropertyTypeRequest
Response: PropertyTypeResponse

GET /property-types/{id}
Desc: Get property type by id
Rules: Authenticated
Response: PropertyTypeResponse

PUT /property-types/{id}
Desc: Update property type
Rules: ADMIN
Request: UpdatePropertyTypeRequest
Response: PropertyTypeResponse

DELETE /property-types/{id}
Desc: Delete property type
Rules: ADMIN
Response: 204 No Content

---

## Organizations
Prefix: `/organizations`

GET /organizations
Desc: List organizations
Rules: Authenticated
Response: OrganizationListResponse

GET /organizations/{org_id}
Desc: Get organization detail
Rules: Authenticated
Response: OrganizationResponse

POST /organizations
Desc: Create organization
Rules: ADMIN
Request: CreateOrganizationRequest
Response: OrganizationResponse

PUT /organizations/{org_id}
Desc: Update organization
Rules: ADMIN
Request: UpdateOrganizationRequest
Response: OrganizationResponse

DELETE /organizations/{org_id}
Desc: Delete organization
Rules: ADMIN
Response: 204 No Content

---

## Users
POST /users
Desc: Create user
Rules: ADMIN
Request: CreateUserRequest
Response: UserResponse

GET /users
Desc: List users
Rules: ADMIN
Params: UserListParams
Response: UserListResponse

GET /users/{user_id}
Desc: Get user detail
Rules: ADMIN
Response: UserResponse

PUT /users/{user_id}
Desc: Update user
Rules: ADMIN
Request: UpdateUserRequest
Response: UserResponse

PATCH /users/{user_id}/deactivate
Desc: Deactivate user
Rules: ADMIN
Response: UserResponse

PATCH /users/{user_id}/reactivate
Desc: Reactivate user
Rules: ADMIN
Response: UserResponse

PATCH /users/{user_id}
Desc: Change partial users fields
Rules: ADMIN only (cannot self-demote from ADMIN)
Request: UpdateUserRoleRequest
Response: UserResponse

---

## Profile

GET /me
Desc: Get my user profile
Rules: Authenticated
Response: ProfileResponse

---

## Properties

POST /properties
Desc: Create property
Rules: Authenticated
Request: CreatePropertyRequest
Response: PropertyResponse

GET /properties
Desc: List all properties (with filters)
Rules: Authenticated
Request Params: PropertyListParams
Response: PropertyListResponse

GET /properties/{id}
Desc: Get property by id
Rules: Authenticated
Response: PropertyResponse

PUT /properties/{id}
Desc: Update property
Rules:
- Accept status: draff, post_pending, available
- When Request User is
  - Sale:
    - Only updatable by owner
    - System changes status to edit_pending
    - System sends notification (request_edit) to approver|admin
  - Admin + Approver:
    - Can update any
    - System reverts status to previous value (before submit to edit)
Request: UpdatePropertyRequest
Response: PropertyResponse

DELETE /properties/{id}
Desc: Delete property
Rules:
- Accept status: any
- When Request User is
  - Sale:
    - Only deletable by owner
  - Admin, Approver:
    - Can delete any property
- Hard delete for: draff, post_pending, available
- Soft delete for: deposit_pending, deposited, soldout_pending, soldout, expired, complete_pending, completed
Response: 204 No Content

POST /properties/{id}/transitions/submit
Desc: Submit property for approval/posting
Rules:
- Accept status: draff
- When Request User is
  - Sale:
    - Only submittable by owner
    - Change status to post_pending
    - System sends notification (request_post) to approver|admin
  - Admin, Approver:
    - Can submit any
    - Change status to available
Request: NotesRequest
Response: PropertyResponse

POST /properties/{id}/transitions/withdraw
Desc: Withdraw property from approval
Rules:
- Accept status: post_pending
- When Request User is
  - Sale:
    - Only withdrawable by owner
    - Change status to draff
  - Admin, Approver:
    - Not needed (can directly submit to available)
Request: NotesRequest
Response: PropertyResponse

POST /properties/{id}/transitions/deposit
Desc: Report deposit / confirm deposit
Rules:
- Accept status: available
- Contract date must >= current date
- File:
  - count <= 10
  - accept image only (image/jpeg, image/png, image/webp)
- Customer phone and name is required
- When Request User is
  - Sale:
    - Change status to deposit_pending
    - Send notification (request_deposit) to admin/approver
  - Admin, Approver:
    - Change status to deposited
Request: DepositRequest
Response: PropertyResponse

POST /properties/{id}/transitions/soldout
Desc: Report sold out / confirm sold out
Rules:
- Accept status: available, deposited
- When Request User is
  - Sale:
    - Change status to soldout_pending
    - Send notification (request_soldout) to admin/approver
  - Admin, Approver:
    - Change status to soldout
Request: NotesRequest
Response: PropertyResponse

POST /properties/{id}/transitions/cancel
Desc: Cancel deposit / confirm cancellation
Rules:
- Accept status: deposited
- When Request User is
  - Sale:
    - Change status to cancel_pending
    - Send notification (request_cancel) to admin/approver
  - Admin, Approver:
    - Change status to available (revert to available)
Request: NotesRequest
Response: PropertyResponse

POST /properties/{id}/transitions/complete
Desc: Complete transaction / confirm completion
Rules:
- Accept status: deposited
- Contract date must >= current date
- File:
  - count <= 10
  - accept image only
- Customer phone and name is required
- When Request User is
  - Sale:
    - Change status to complete_pending
    - Send notification (request_complete) to admin/approver
  - Admin, Approver:
    - Change status to completed
Request: CompleteRequest
Response: PropertyResponse

GET /properties/{id}/status-logs
Desc: Get property status change history
Rules:
- Only owner and admin/approver roles can see
Response: StatusLogResponse

---

## Reviews

GET /properties/{id}/reviews
Desc: List reviews for a property
Rules: Authenticated
Response: ReviewListResponse

GET /properties/{id}/reviews/{review_id}
Desc: Get review detail
Rules: Authenticated
Response: ReviewDetailResponse

POST /properties/{id}/reviews
Desc: Create review for a property
Rules: Authenticated (one review per author per property)
Request: CreateReviewRequest
Response: ReviewDetailResponse

DELETE /properties/{id}/reviews/{review_id}
Desc: Delete a review
Rules: Only owner or admin can delete
Response: 204 No Content

---

## Hot Properties

GET /properties/hots
Desc: List currently active hot properties
Rules: Any
Response: HotPropertyListResponse

POST /properties/{id}/hots
Desc: Promote a property to hot
Rules: Admin
Request: PromoteToHotRequest
Response: HotPropertyResponse

DELETE /properties/{id}/hots
Desc: Remove a property from hot
Rules: Admin
Response: 204 No Content

---

## Pins

### Replacement
POST /properties/{id}/pins
Desc: Add property to my pins
Rules: Any authenticated
Response: PinResponse

DELETE /properties/{id}/pins
Desc: Remove property from my pins
Rules: Any authenticated
Response: 204 No Content

---

## Notifications
Prefix: `/notifications`

GET /notifications
Desc: List my notifications
Rules: Authenticated
Params: NotificationListParams
Response: NotificationListResponse

GET /notifications/unread-count
Desc: Get unread notification count
Rules: Authenticated
Response: NotificationCountResponse

PATCH /notifications/{id}/read
Desc: Mark notification as read
Rules: Authenticated (owner only)
Response: NotificationResponse

POST /notifications/read-all
Desc: Mark all notifications as read
Rules: Authenticated
Response: ReadAllResponse

---

## Approvals

GET /approvals
Desc: List approvals
Rules: Only admin/approver can access
Request Params: ApprovalListParams
Response: ApprovalListResponse

GET /approvals/counts
Desc: Get approval counts by release type
Rules: Only admin/approver can access
Response: ApprovalCountsResponse

GET /approvals/{id}
Desc: Get approval detail
Rules: Only admin/approver can access
Response: ApprovalDetailResponse

POST /approvals/{id}/transitions/approve
Desc: Approve a pending request
Rules:
- Only admin/approver can access
- Accept approval status: pending
Request: ApproveRequest
Response: ApprovalDetailResponse

POST /approvals/{id}/transitions/reject
Desc: Reject a pending request
Rules:
- Only admin/approver can access
- Accept approval status: pending
Request: RejectRequest
Response: ApprovalDetailResponse

---

## My Assets

GET /me/properties
Desc: List my properties
Rules: Authenticated
Params: & PropertyFilterRequest
Response: MyPropertyListResponse

GET /me/pins
Desc: List my pinned properties
Rules: Authenticated
Response: MyPinListResponse

---

## Notification Preferences

GET /me/notification-preferences
Desc: Get my notification preferences
Rules: Authenticated
Response: NotificationPrefsResponse

PUT /me/notification-preferences
Desc: Update my notification preferences
Rules: Authenticated
Request: UpdateNotificationPrefsRequest
Response: NotificationPrefsResponse

---