# Story: Approve Deposit Report

## User Story

As an Approver
I want to confirm a reported deposit
So that the listing is officially marked as deposited and unavailable for other customers

## Description

Deposit reports appear in the "Duyệt báo cọc" approval queue. The approver
reviews the details and confirms or rejects the deposit.

## Preconditions

- User is logged in as Approver or Admin
- A deposit report exists on a listing

## Acceptance Criteria

### Happy Path

Given I am on the deposit approval queue
When I review a deposit report and click "Confirm"
Then the listing status changes to DEPOSITED
And the agent who reported receives a confirmation notification

### Validation Rules

Given I reject the deposit
When I enter a reason and confirm
Then the listing returns to ACTIVE status
And the agent receives a rejection notification

## Business Rules

- BR-005

## Related Entities

- Listing
- DealEvent
- Approval
- Notification

## Priority

Must Have
