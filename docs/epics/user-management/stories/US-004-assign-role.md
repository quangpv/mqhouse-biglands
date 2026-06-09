# Story: Assign User Role

## User Story

As an Admin
I want to change a user's role
So that they have appropriate permissions

## Description

Admin can change any user's role among AGENT, APPROVER, and ADMIN.

## Preconditions

- User is logged in as Admin
- Cannot change the role of the last remaining ADMIN

## Acceptance Criteria

### Happy Path

Given I am editing a user
When I change their role from AGENT to APPROVER
Then the user's permissions are updated immediately
And the user sees the new menu options on next page load

### Validation Rules

Given I attempt to change the last ADMIN's role to AGENT
When I save
Then I see an error: "Cannot change role of the only admin"

## Related Entities

- User

## Priority

Should Have
