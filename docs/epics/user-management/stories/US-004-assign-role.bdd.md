# BDD: Assign User Role

> **Story**: US-004-assign-role
> **Priority**: Should Have
> **Related**: User entity, UM-002, UM-003
> **Contradiction Note**: AR-13 (role display vs organization names)

## Acceptance Criteria
- Admin can change any user's role among AGENT, APPROVER, ADMIN
- Role change takes effect immediately
- User sees new menu options on next page load
- Cannot change role of the last ADMIN

## Happy Paths

### H1: Change role from AGENT to APPROVER
```
Given I am logged in as Admin
And I am editing an AGENT user
When I change their role from "AGENT" to "APPROVER"
And I click "Save"
Then the user's role is updated to APPROVER
And the user sees new approval queue menu items on next page load
```

### H2: Change role from APPROVER to ADMIN
```
Given I am editing an APPROVER user
When I change their role to "ADMIN"
And I click "Save"
Then the user gains full admin capabilities
And sees the full sidebar on next page load
```

### H3: Demote ADMIN to AGENT (when other ADMINs exist)
```
Given there are 3 ADMIN users on the platform
When I change one ADMIN's role to "AGENT"
And I click "Save"
Then the user's role is updated to AGENT
And the user loses admin privileges immediately
```

## Error Cases

### E1: Change role of the last ADMIN
```
Given there is exactly one ADMIN user
When I attempt to change that ADMIN's role to "AGENT"
Then I see "Cannot change role of the only admin"
And the user remains ADMIN
```

## Edge Cases

### EC1: Role change during active session
```
Given I am an AGENT currently browsing
When an Admin changes my role to APPROVER
Then on my next page navigation, I see the new sidebar items
And I can access approval queues
```

### EC2: Role change back to same role
```
Given a user is APPROVER
When I change their role from APPROVER to APPROVER
And I click "Save"
Then the user's role remains APPROVER
And no unnecessary update is recorded
```

### EC3: Immediate permission enforcement
```
Given an APPROVER has an approval queue page open
When an Admin changes their role to AGENT
Then on the APPROVER's next API call, they receive 403
And they are redirected away from the approval queue
```

## Security Cases

### S1: Agent attempts to change role
```
Given I am logged in as Agent
When I attempt to change any user's role
Then I see 403 Forbidden
```

### S2: Approver attempts to change role
```
Given I am logged in as Approver
When I attempt to change any user's role via API
Then the request is rejected with HTTP 403
```

### S3: Self-elevation attempt
```
Given I am an AGENT
When I attempt to modify my own role via API manipulation
Then the request is rejected
```
