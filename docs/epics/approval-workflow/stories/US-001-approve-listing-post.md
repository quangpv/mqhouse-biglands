# Story: Approve Listing Post

## User Story

As an Approver
I want to approve a pending listing post
So that it becomes visible to all agents in the shared cart

## Description

A queue page shows all listings submitted for approval. The approver can view
the full listing detail and either approve (making it ACTIVE) or reject
(returning to DRAFT with a reason).

## Preconditions

- User is logged in as Approver or Admin
- There are listings in PENDING_APPROVAL status

## Acceptance Criteria

### Happy Path

Given I am an Approver
When I navigate to the approval queue for a transaction type
Then I see a list of listings pending approval
When I click on a listing
Then I see the full listing details
When I click "Approve"
Then the listing status changes to ACTIVE
And the listing agent receives a notification

### Validation Rules

Given I attempt to approve a listing with missing required data
When I click "Approve"
Then I see an error message

### Error Cases

Given two approvers attempt to approve the same listing simultaneously
When both click "Approve"
Then only one succeeds and the other sees a "Already processed" message

## Business Rules

- BR-005
- BR-006

## Related Entities

- Listing
- Approval
- Notification

## Priority

Must Have
