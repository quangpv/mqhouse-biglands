# BDD: Create User Account

> **Story**: US-001-create-user
> **Priority**: Must Have
> **Related**: User entity, UM-002, UM-006
> **Contradiction Note**: AR-13 (role display vs enum in user list)

## Acceptance Criteria
- Admin can create a user with full name, username, phone (optional), and role
- Username must be unique
- An initial password is generated
- Created user appears in the user list and can log in

## Happy Paths

### H1: Create user with all required fields
```
Given I am logged in as Admin
When I navigate to User Management
And I click "Create User"
Then I see a form with fields: full name, username, phone, role
When I fill in full name "Nguyễn Văn A"
And I fill in username "nguyenvana"
And I select role "AGENT"
And I submit the form
Then the user account is created
And I see the new user in the user list
And a password is generated for the user
```

### H2: Create user with optional phone number
```
Given I am logged in as Admin
When I fill in all required fields
And I enter phone "0909123456"
And I submit
Then the user is created with phone number saved
```

### H3: Create user as APPROVER role
```
Given I am logged in as Admin
When I select role "APPROVER"
And I fill in all required fields
And I submit
Then a user with APPROVER role is created
```

## Error Cases

### E1: Duplicate username
```
Given a user with username "nguyenvana" already exists
When I enter username "nguyenvana"
And I submit
Then I see "Username already exists"
```

### E2: Missing role
```
Given I do not select a role
When I submit
Then I see "Role is required"
```

### E3: Missing full name
```
Given I leave full name empty
When I submit
Then I see a validation error on the full name field
```

### E4: Missing username
```
Given I leave username empty
When I submit
Then I see a validation error on the username field
```

## Edge Cases

### EC1: Maximum-length field values
```
Given I enter a full name exactly at the character limit
And I enter a username at the character limit
When I submit
Then the user is created with the exact values
```

### EC2: Username with special characters
```
Given I enter a username containing special characters
When I submit
Then the system validates against allowed username format
```

### EC3: Self-creation attempt
```
Given there is only one Admin user currently
When that Admin attempts to create themselves again (duplicate username)
Then the system rejects with duplicate username error
```

## Security Cases

### S1: Agent attempts to create user
```
Given I am logged in as Agent
When I navigate to /admin/quan-ly-nguoi-dung
Then I see "Bạn không có quyền truy cập trang này"
```

### S2: Approver attempts to create user
```
Given I am logged in as Approver
When I attempt to access the user creation API
Then the request is rejected with HTTP 403
```

### S3: Unauthenticated access
```
Given I am not logged in
When I navigate to /admin/quan-ly-nguoi-dung/tao
Then I am redirected to the login page
```

### S4: Direct API call without permissions
```
Given I have a valid Agent session token
When I send a POST request to the user creation API
Then the response is HTTP 403 Forbidden
```
