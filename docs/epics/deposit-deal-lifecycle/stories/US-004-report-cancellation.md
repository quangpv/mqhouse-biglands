# Story: Report Deposit Cancellation

## User Story

As an Agent
I want to report that the customer has cancelled their deposit
So that the property becomes available again for other customers

## Description

If a deal falls through, the agent reports "Báo khách huỷ cọc" (Report
Cancellation) with a reason. This creates a Cancellation Reported event
pending approval.

## Preconditions

- User is logged in as Agent
- Listing status is DEPOSITED

## Acceptance Criteria

### Happy Path

Given my listing has a confirmed deposit
When I click "Báo khách huỷ cọc"
Then I am prompted to enter a reason
When I enter the reason and submit
Then a cancellation report event is created
And the listing status changes to CANCELLED (pending approval)

### Validation Rules

Given I attempt to submit cancellation without a reason
When I click submit
Then I see a validation error: "Cancellation reason is required"

## Business Rules

- BR-002
- BR-004

## Related Entities

- Listing
- DealEvent

## Priority

Should Have
