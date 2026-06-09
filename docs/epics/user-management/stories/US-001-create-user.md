# Story: Create User Account

## User Story

As an Admin
I want to create a new user account
So that new agents can access the platform

## Description

The admin fills in the user's full name, username, phone number (optional), and selects a role.
An initial password is generated. The user receives their credentials via
notification or the admin shares them directly.

## Preconditions

- User is logged in as Admin

## Acceptance Criteria

### Happy Path

Given I am an Admin
When I navigate to User Management and click "Create User"
Then I see a form with fields: full name, username, phone, role
When I fill in valid data and submit
Then the user account is created
And I see the user in the user list
And the user can log in with their username and initial password

### Validation Rules

Given I enter a username that already exists
When I submit
Then I see an error: "Username already exists"

Given I do not select a role
When I submit
Then I see a validation error: "Role is required"

## Related Entities

- User

## Priority

Must Have
