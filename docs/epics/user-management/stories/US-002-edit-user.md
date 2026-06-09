# Story: Edit User Profile

## User Story

As an Admin
I want to edit a user's profile details
So that I can update their name, username, or reset their password

## Description

Admin can update user full name, username, phone number, and reset password.

## Preconditions

- User is logged in as Admin

## Acceptance Criteria

### Happy Path

Given I am viewing the user list
When I click "Edit" on a user
Then I see the user's current details pre-filled
When I modify the name and click "Save"
Then the user's details are updated

## Related Entities

- User

## Priority

Should Have
