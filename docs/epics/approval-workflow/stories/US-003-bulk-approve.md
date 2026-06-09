# Story: Bulk Approve Listings

## User Story

As an Approver
I want to approve multiple listings at once
So that I can process high volumes efficiently

## Description

The approval queue supports selecting multiple listings and approving them
in a single action. Rejection is always individual with a specific reason.

## Preconditions

- User is logged in as Approver or Admin
- At least 2 listings are pending approval

## Acceptance Criteria

### Happy Path

Given I am on the approval queue page
When I select multiple listings using checkboxes
When I click "Approve Selected"
Then all selected listings become ACTIVE
And each listing agent receives a notification

### Validation Rules

Given I select 0 listings
When I click "Approve Selected"
Then I see a message: "Please select at least one listing"

## Business Rules

- BR-005

## Related Entities

- Listing
- Approval
- Notification

## Priority

Could Have
