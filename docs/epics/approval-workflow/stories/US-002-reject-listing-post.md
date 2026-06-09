# Story: Reject Listing Post

## User Story

As an Approver
I want to reject a listing with a reason
So that the agent knows what to fix before resubmitting

## Description

When an approver rejects a listing, it returns to DRAFT status with the
rejection reason visible to the agent.

## Preconditions

- User is logged in as Approver or Admin
- Listing is in PENDING_APPROVAL status

## Acceptance Criteria

### Happy Path

Given I am viewing a pending listing
When I click "Reject"
Then I am prompted to enter a rejection reason
When I enter the reason and confirm
Then the listing returns to DRAFT status
And the agent receives a notification with the rejection reason

### Validation Rules

Given I click "Reject" without entering a reason
When I try to confirm
Then I see a validation error: "Rejection reason is required"

## Business Rules

- BR-005
- BR-006

## Related Entities

- Listing
- Approval
- Notification

## Priority

Must Have
