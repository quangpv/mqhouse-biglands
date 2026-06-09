# Story: Mark Listing as Sold-Out

## User Story

As an Agent
I want to report that my listing is sold out
So that it is removed from the active pool

## Description

When the property is sold or fully rented without a deposit track record,
the agent can report "Báo hết hàng" (Report Sold-Out). After approval, the
listing is permanently marked as SOLD_OUT.

## Preconditions

- User is logged in as Agent
- Listing belongs to current user
- Listing status is ACTIVE

## Acceptance Criteria

### Happy Path

Given I have an ACTIVE listing
When I click "Báo hết hàng"
Then I am asked to confirm
When I confirm
Then a sold-out report event is created
And the listing status changes to SOLD_OUT (pending approval)
And approvers are notified

### Permission Rules

Given I am viewing another agent's listing
When I look for the sold-out button
Then the button is not visible

## Business Rules

- BR-004

## Related Entities

- Listing
- DealEvent

## Priority

Must Have
