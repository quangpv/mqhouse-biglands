# Story: Approve Cancellation

## User Story

As an Approver
I want to confirm a cancellation report
So that the property is returned to the active pool

## Description

Cancellation reports appear in the "Duyệt huỷ cọc" approval queue. The
approver reviews the reason and confirms or rejects.

## Preconditions

- User is logged in as Approver or Admin
- A cancellation report exists on a listing

## Acceptance Criteria

### Happy Path

Given I am on the cancellation approval queue
When I review a cancellation and click "Confirm"
Then the listing returns to ACTIVE status
And the agent receives a confirmation notification

## Business Rules

- BR-005

## Related Entities

- Listing
- Approval
- Notification

## Priority

Should Have
