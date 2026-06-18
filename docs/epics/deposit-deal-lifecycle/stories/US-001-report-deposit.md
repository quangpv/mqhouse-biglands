# Story: Report Customer Deposit

## User Story

As an Agent
I want to report that a customer has placed a deposit on a listing
So that the deposit is recorded and other agents know the property is pending

## Description

On the listing detail page, the agent clicks "Báo khách cọc" (Report Deposit)
and enters the customer name, phone number, and deposit amount. This creates a
Deposit Reported event and notifies approvers.

## Preconditions

- User is logged in as Agent
- Listing status is ACTIVE
- No active deposit exists on this listing

## Acceptance Criteria

### Happy Path

Given I am viewing an ACTIVE listing
When I click "Báo khách cọc"
Then I see a form for customer name, phone, and deposit amount
When I fill in the fields and submit
Then a deposit report event is created
And the listing status changes to DEPOSITED (pending approval)
And approvers are notified

### Validation Rules

Given I enter a customer name with fewer than 2 characters
When I submit the deposit report
Then I see a validation error

Given the deposit amount is zero or negative
When I submit the deposit report
Then I see a validation error

### Error Cases

Given another agent already reported a deposit on the same listing (not yet approved)
When I attempt to report a deposit
Then I see an error: "A deposit is already pending on this listing"

## Business Rules

- BR-001
- BR-004

## Related Entities

- Listing
- DealEvent

## Priority

Must Have
