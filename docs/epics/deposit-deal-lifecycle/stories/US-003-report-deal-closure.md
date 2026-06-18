# Story: Report Deal Closure

## User Story

As an Agent
I want to report that the deal is closed with the customer
So that the property is marked as closed and commission can be processed

## Description

After a deposit is confirmed, the agent can report "Báo khách chốt hàng" (Report
Deal Closure). This creates a Closure Reported event pending approval.

## Preconditions

- User is logged in as Agent
- Listing status is DEPOSITED (deposit confirmed)

## Acceptance Criteria

### Happy Path

Given my listing has a confirmed deposit
When I click "Báo khách chốt hàng"
Then a closure report event is created
And the listing status changes to CLOSED (pending approval)

### Error Cases

Given my listing is ACTIVE (no deposit)
When I look for the closure button
Then the button is disabled or hidden

## Business Rules

- BR-003
- BR-004

## Related Entities

- Listing
- DealEvent

## Priority

Should Have
