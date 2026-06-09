# Story: Deactivate/Reactivate User

## User Story

As an Admin
I want to deactivate a user who no longer works with us
So that they cannot access the platform

## Description

Admin can toggle a user between active and inactive. Inactive users cannot log
in. Their existing listings remain visible but they cannot create new ones.

## Preconditions

- User is logged in as Admin
- Target user is not the only ADMIN

## Acceptance Criteria

### Happy Path

Given I am editing a user
When I toggle the "Active" switch to off
Then the user is deactivated
And the user cannot log in

Given the user is deactivated
When I toggle "Active" back to on
Then the user is reactivated
And the user can log in again

### Validation Rules

Given I attempt to deactivate the only ADMIN user
When I toggle "Active" to off
Then I see an error: "Cannot deactivate the only admin"

## Related Entities

- User

## Priority

Must Have
