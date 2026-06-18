# BDD: Deactivate/Reactivate User

> **Story**: US-003-deactivate-user
> **Priority**: Must Have
> **Related**: User entity, UM-001, UM-002, UM-004, UM-005

## Acceptance Criteria
- Admin can toggle a user between active and inactive
- Inactive users cannot log in
- Inactive users' existing listings remain visible
- Cannot deactivate the last ADMIN
- Cannot deactivate own account

## Happy Paths

### H1: Deactivate a user
```
Given I am logged in as Admin
And I am editing an active user who is not the last ADMIN
When I toggle the "Active" switch to off
Then the user is deactivated
And the user's status shows "Inactive"
```

### H2: Reactivate a user
```
Given a user is deactivated
When I toggle "Active" back to on
Then the user is reactivated
And the user can log in again
```

### H3: Deactivated user cannot log in
```
Given a user has been deactivated
When that user attempts to log in with valid credentials
Then they see an error: "Account has been deactivated. Contact your admin."
```

### H4: Deactivated user's listings remain visible
```
Given a user has been deactivated
When other agents browse the shared cart
Then the deactivated user's existing listings are still visible
```

## Error Cases

### E1: Deactivate the only ADMIN
```
Given there is exactly one ADMIN user on the platform
When I toggle "Active" to off on that ADMIN
Then I see "Cannot deactivate the only admin"
And the user remains active
```

### E2: Admin attempts to deactivate own account
```
Given I am the only ADMIN
When I attempt to deactivate my own account
Then I see an error
And my account remains active
```

## Edge Cases

### EC1: Deactivated user tries to create a listing
```
Given my account is deactivated
When I attempt to log in
Then I cannot log in
And I cannot create new listings
```

### EC2: Rapid toggle deactivate/reactivate
```
Given I deactivate a user
When I immediately reactivate them
Then the user is active
And the user can log in
```

### EC3: Bulk deactivation (if multiple Admin exist)
```
Given there are 3 ADMIN users
When I deactivate one ADMIN
Then the other 2 ADMINs remain
And the platform continues to function
```

## Security Cases

### S1: Non-admin attempts to deactivate
```
Given I am logged in as Agent
When I attempt to deactivate any user
Then I see 403 Forbidden
```

### S2: Stolen session after deactivation
```
Given a user's account is deactivated
When that user's existing session attempts an API call
Then the session is invalidated
And the request is rejected with 401
```
