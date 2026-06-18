# BDD: Edit User Profile

> **Story**: US-002-edit-user
> **Priority**: Should Have
> **Related**: User entity

## Acceptance Criteria
- Admin can edit a user's full name, username, phone number
- Admin can reset a user's password
- Edit form is pre-filled with current user data

## Happy Paths

### H1: Edit user full name
```
Given I am logged in as Admin
And I am viewing the user list
When I click "Edit" on a user
Then I see the user's current details pre-filled
When I modify the full name
And I click "Save"
Then the user's details are updated
```

### H2: Edit username
```
Given I am editing a user
When I change their username to a unique value
And I click "Save"
Then the username is updated
And the user can log in with the new username
```

### H3: Reset user password
```
Given I am editing a user
When I click "Reset Password"
Then a new password is generated
And the password hash is updated
```

### H4: Edit phone number
```
Given I am editing a user who has no phone
When I enter a phone number
And I click "Save"
Then the phone number is saved
```

## Error Cases

### E1: Edit username to an existing one
```
Given another user has username "existing_user"
When I change the current user's username to "existing_user"
And I click "Save"
Then I see "Username already exists"
```

## Edge Cases

### EC1: Edit nothing (submit without changes)
```
Given I am editing a user
When I click "Save" without making any changes
Then the user data remains unchanged
And no update is recorded
```

### EC2: Clear phone number (set to empty)
```
Given a user has a phone number saved
When I clear the phone field
And I click "Save"
Then the phone is cleared (set to null/empty)
```

## Security Cases

### S1: Agent attempts to edit user
```
Given I am logged in as Agent
When I attempt to access the user edit API
Then the request is rejected with HTTP 403
```

### S2: Approver attempts to edit user
```
Given I am logged in as Approver
When I attempt to access the user edit API
Then the request is rejected with HTTP 403
```

### S3: Unauthenticated access
```
Given I am not logged in
When I attempt to access /admin/quan-ly-nguoi-dung/:id/sua
Then I am redirected to the login page
```
